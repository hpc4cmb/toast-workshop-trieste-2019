import toast
import toast.todmap
from toast.mpi import MPI

import numpy as np
import matplotlib.pyplot as plt

from toast.tod import hex_pol_angles_radial, hex_pol_angles_qu, hex_layout

def fake_focalplane(
    samplerate=20,
    epsilon=0,
    net=1,
    fmin=0,
    alpha=1,
    fknee=0.05,
    fwhm=30,
    npix=7,
    fov=3.0
):
    """Create a set of fake detectors.

    This generates 7 pixels (14 dets) in a hexagon layout at the boresight
    and with a made up polarization orientation.

    Args:
        None

    Returns:
        (dict):  dictionary of detectors and their properties.

    """
    zaxis = np.array([0, 0, 1.0])
    
    pol_A = hex_pol_angles_qu(npix)
    pol_B = hex_pol_angles_qu(npix, offset=90.0)
    
    dets_A = hex_layout(npix, fov, "", "", pol_A)
    dets_B = hex_layout(npix, fov, "", "", pol_B)
    
    dets = dict()
    for p in range(npix):
        pstr = "{:01d}".format(p)
        for d, layout in zip(["A", "B"], [dets_A, dets_B]):
            props = dict()
            props["quat"] = layout[pstr]["quat"]
            props["epsilon"] = epsilon
            props["rate"] = samplerate
            props["alpha"] = alpha
            props["NET"] = net
            props["fmin"] = fmin
            props["fknee"] = fknee
            props["fwhm_arcmin"] = fwhm
            dname = "{}{}".format(pstr, d)
            dets[dname] = props
    return dets


mpiworld, procs, rank = toast.mpi.get_world()
comm = toast.mpi.Comm(mpiworld)

# A pipeline would create the args object with argparse

class args:
    sample_rate = 10  # Hz
    hwp_rpm = None
    hwp_step_deg = None
    hwp_step_time_s = None
    spin_period_min = 1 # 10
    spin_angle_deg = 20 # 30
    prec_period_min = 100 # 50
    prec_angle_deg = 30 # 65
    coord = "E"
    nside = 64
    nnz = 3
    outdir = "maps"

# Create a fake focalplane, we could also load one from file.
# The Focalplane class interprets the focalplane dictionary
# created by fake_focalplane() but it can also load the information
# from file.

focalplane = fake_focalplane(samplerate=args.sample_rate, fknee=0.1, alpha=2)
detectors = sorted(focalplane.keys())
detquats = {}
for d in detectors:
    detquats[d] = focalplane[d]["quat"]
    
nsample = 100000
start_sample = 0
start_time = 0
iobs = 0

tod = toast.todmap.TODSatellite(
    comm.comm_group,
    detquats,
    nsample,
    coord=args.coord,
    firstsamp=start_sample,
    firsttime=start_time,
    rate=args.sample_rate,
    spinperiod=args.spin_period_min,
    spinangle=args.spin_angle_deg,
    precperiod=args.prec_period_min,
    precangle=args.prec_angle_deg,
    detranks=comm.group_size,
    hwprpm=args.hwp_rpm,
    hwpstep=args.hwp_step_deg,
    hwpsteptime=args.hwp_step_time_s,
)

# Constantly slewing precession axis                                                                                                                                             
precquat = np.empty(4 * tod.local_samples[1], dtype=np.float64).reshape((-1, 4))
toast.todmap.slew_precession_axis(
    precquat,
    firstsamp=start_sample + tod.local_samples[0],
    samplerate=args.sample_rate,
    degday=360.0 / 365.25,
)
tod.set_prec_axis(qprec=precquat)

noise = toast.pipeline_tools.get_analytic_noise(args, comm, focalplane)

obs = {}
obs["name"] = "science_{:05d}".format(iobs)
obs["tod"] = tod
obs["intervals"] = None
obs["baselines"] = None
obs["noise"] = noise
obs["id"] = iobs

data = toast.Data(comm)
data.obs.append(obs)

# Simulate noise
simnoise = toast.tod.OpSimNoise(out="signal", realization=0)
toast.tod.OpCacheClear("noise").exec(data)
simnoise.exec(data)

# Get pixel numbers

toast.todmap.OpPointingHpix(nside=args.nside, nest=True, mode="IQU").exec(data)

# Bin a map

mapmaker = toast.todmap.OpMapMaker(
    nside=args.nside,
    nnz=3,
    name="signal",
    outdir=args.outdir,
    outprefix="toast_test_",
    baseline_length=None,
    # maskfile=self.maskfile_binary,
    # weightmapfile=self.maskfile_smooth,
    # subharmonic_order=None,
    iter_max=100,
    use_noise_prior=False,
    # precond_width=30,
    write_wcov_inv=False,
    write_wcov=False,
    write_binned=False,
    write_rcond=False,
)
mapmaker.exec(data)

# Plot the hits

import healpy as hp

hitmap = hp.read_map("maps/toast_test_hits.fits")
nhit = np.sum(hitmap)
print("{} total hits".format(nhit))
hitmap[hitmap == 0] = hp.UNSEEN
hp.mollview(hitmap, title="{} total hits".format(nhit))
plt.savefig("hits.png")
