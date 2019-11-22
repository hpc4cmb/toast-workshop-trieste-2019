NB=$1
jupyter nbconvert $NB --to python --stdout | grep -v ipython > ${NB/ipynb/py}
