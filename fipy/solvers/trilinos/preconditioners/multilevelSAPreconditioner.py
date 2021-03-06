from __future__ import unicode_literals
__docformat__ = 'restructuredtext'

from PyTrilinos import ML

from fipy.solvers.trilinos.preconditioners.preconditioner import Preconditioner

__all__ = ["MultilevelSAPreconditioner"]
from future.utils import text_to_native_str
__all__ = [text_to_native_str(n) for n in __all__]

class MultilevelSAPreconditioner(Preconditioner):
    """
    Multilevel preconditioner for Trilinos solvers suitable classical
    smoothed aggregation for symmetric positive definite or nearly
    symmetric positive definite systems.
    """

    def _applyToSolver(self, solver, matrix):
        if matrix.NumGlobalNonzeros() <= matrix.NumGlobalRows():
            return

        self.Prec = ML.MultiLevelPreconditioner(matrix, False)

        self.Prec.SetParameterList({text_to_native_str("output"): 0,
                                    text_to_native_str("max levels") : 10,
                                    text_to_native_str("prec type") : text_to_native_str("MGV"),
                                    text_to_native_str("increasing or decreasing") : text_to_native_str("increasing"),
                                    text_to_native_str("aggregation: type") : text_to_native_str("Uncoupled-MIS"),
                                    text_to_native_str("aggregation: damping factor") : 4. / 3.,
##                                    "energy minimization: enable" : False,
##                                    "smoother: type" : "Aztec",
##                                    "smoother: type" : "symmetric Gauss-Seidel",
##                                    "eigen-analysis: type" : "power-method",
                                    text_to_native_str("eigen-analysis: type") : text_to_native_str("cg"),
                                    text_to_native_str("eigen-analysis: iterations") : 10,
                                    text_to_native_str("smoother: sweeps") : 2,
                                    text_to_native_str("smoother: damping factor") : 1.0,
                                    text_to_native_str("smoother: pre or post") : text_to_native_str("both"),
                                    text_to_native_str("smoother: type") : text_to_native_str("symmetric Gauss-Seidel"),
                                    text_to_native_str("coarse: type") : text_to_native_str("Amesos-KLU"),
                                    text_to_native_str("coarse: max size") : 128
                                    })

        self.Prec.ComputePreconditioner()

        solver.SetPrecOperator(self.Prec)
