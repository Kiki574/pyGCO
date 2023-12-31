import ctypes as ct
import os
from glob import glob

import numpy as np

_LIB_BASE_NAME = "libcgco"
_LIB_EXTENSIONS = (".so", ".pyd", ".dll")
# or change this to your own path that contains libcgco.so
_CGCO_LIB_PATH = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
assert os.path.isdir(_CGCO_LIB_PATH)

_LIBGCO_PATTER = os.path.join(_CGCO_LIB_PATH, _LIB_BASE_NAME + ".*")
_LIST_LIBGCO = glob(_LIBGCO_PATTER)
if not _LIST_LIBGCO:
    raise FileNotFoundError("no compiled library found in %s" % repr(_LIBGCO_PATTER))

_CGCO_LIB_NAMES = [os.path.basename(pl) for pl in _LIST_LIBGCO if os.path.splitext(pl)[1] in _LIB_EXTENSIONS]
if not _CGCO_LIB_NAMES:  # not sure what it found...
    raise RuntimeError("found potential libs: %s" % repr(_LIST_LIBGCO))
_CGCO_LIB_NAME = _CGCO_LIB_NAMES[0]

# change the type definition depending on your machine and the compiled GCO library
_handle_type = ct.c_int
_handle_ptr_type = np.ctypeslib.ndpointer(dtype=np.intc)
_site_id_type = ct.c_int
_site_ptr_type = np.ctypeslib.ndpointer(dtype=np.intc)
_label_id_type = ct.c_int
_label_ptr_type = np.ctypeslib.ndpointer(dtype=np.intc)
_energy_term_type = ct.c_int
_energy_term_ptr_type = np.ctypeslib.ndpointer(dtype=np.intc)
# _energy_type = ct.c_int       # if energy32 is set
_energy_type = ct.c_longlong  # default type long long
# _energy_ptr_type = np.ctypeslib.ndpointer(dtype=np.intc)
_energy_ptr_type = np.ctypeslib.ndpointer(dtype=np.longlong)
_success_ptr_type = np.ctypeslib.ndpointer(dtype=np.intc)

_SMOOTH_COST_FN = ct.CFUNCTYPE(_energy_term_type, ct.c_int, ct.c_int, _label_id_type, _label_id_type)

# load cgco shared library
# see: https://catherineh.github.io/programming/2016/07/07/troubleshooting-windows-dll-imports-in-python
_cgco = np.ctypeslib.load_library(_CGCO_LIB_NAME, _CGCO_LIB_PATH)

# declare the functions, argument types and return types
_cgco.gcoCreateGeneralGraph.argtypes = [_site_id_type, _label_id_type, _handle_ptr_type]
_cgco.gcoCreateGeneralGraph.restypes = ct.c_int

_cgco.gcoDestroyGraph.argtypes = [_handle_type]
_cgco.gcoDestroyGraph.restypes = ct.c_int

_cgco.gcoSetDataCost.argtypes = [_handle_type, _energy_term_ptr_type]
_cgco.gcoSetDataCost.restypes = ct.c_int

_cgco.gcoSetSiteDataCost.argtypes = [_handle_type, _site_id_type, _label_id_type, _energy_term_type]
_cgco.gcoSetSiteDataCost.restypes = ct.c_int

_cgco.gcoSetNeighborPair.argtypes = [_handle_type, _site_id_type, _site_id_type, _energy_term_type]
_cgco.gcoSetNeighborPair.restypes = ct.c_int

_cgco.gcoSetAllNeighbors.argtypes = [_handle_type, _site_ptr_type, _site_ptr_type, _energy_term_ptr_type, ct.c_int]
_cgco.gcoSetAllNeighbors.restypes = ct.c_int

_cgco.gcoSetSmoothCost.argtypes = [_handle_type, _energy_term_ptr_type]
_cgco.gcoSetSmoothCost.restype = ct.c_int

_cgco.gcoSetPairSmoothCost.argtypes = [_handle_type, _label_id_type, _label_id_type, _energy_term_type]
_cgco.gcoSetPairSmoothCost.restypes = ct.c_int

_cgco.gcoSetSmoothCostFunction.argtypes = [_handle_type, _SMOOTH_COST_FN]
_cgco.gcoSetSmoothCostFunction.restypes = ct.c_int

_cgco.gcoExpansion.argtypes = [_handle_type, ct.c_int, _energy_ptr_type]
_cgco.gcoExpansion.restypes = ct.c_int

_cgco.gcoExpansionOnAlpha.argtypes = [_handle_type, _label_id_type, _success_ptr_type]
_cgco.gcoExpansionOnAlpha.restypes = ct.c_int

_cgco.gcoSwap.argtypes = [_handle_type, ct.c_int, _energy_ptr_type]
_cgco.gcoSwap.restypes = ct.c_int

_cgco.gcoAlphaBetaSwap.argtypes = [_handle_type, _label_id_type, _label_id_type]
_cgco.gcoAlphaBetaSwap.restypes = ct.c_int

_cgco.gcoComputeEnergy.argtypes = [_handle_type, _energy_ptr_type]
_cgco.gcoComputeEnergy.restypes = ct.c_int

_cgco.gcoComputeDataEnergy.argtypes = [_handle_type, _energy_ptr_type]
_cgco.gcoComputeDataEnergy.restypes = ct.c_int

_cgco.gcoComputeSmoothEnergy.argtypes = [_handle_type, _energy_ptr_type]
_cgco.gcoComputeSmoothEnergy.restypes = ct.c_int

_cgco.gcoGetLabelAtSite.argtypes = [_handle_type, _site_id_type, _label_ptr_type]
_cgco.gcoGetLabelAtSite.restypes = ct.c_int

_cgco.gcoGetLabels.argtypes = [_handle_type, _label_ptr_type]
_cgco.gcoGetLabels.restype = ct.c_int

_cgco.gcoInitLabelAtSite.argtypes = [_handle_type, _site_id_type, _label_id_type]
_cgco.gcoInitLabelAtSite.restypes = ct.c_int
