"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from cvxpy.atoms.affine.affine_atom import AffAtom
from cvxpy.atoms.affine.vec import vec
import cvxpy.lin_ops.lin_utils as lu
import numpy as np


def diag(expr):
    """Extracts the diagonal from a matrix or makes a vector a diagonal matrix.

    Parameters
    ----------
    expr : Expression or numeric constant
        A vector or square matrix.

    Returns
    -------
    Expression
        An Expression representing the diagonal vector/matrix.
    """
    expr = AffAtom.cast_to_const(expr)
    if expr.is_vector():
        return diag_vec(vec(expr))
    elif expr.ndim == 2 and expr.shape[0] == expr.shape[1]:
        return diag_mat(expr)
    else:
        raise ValueError("Argument to diag must be a vector or square matrix.")


class diag_vec(AffAtom):
    """Converts a vector into a diagonal matrix.
    """

    def __init__(self, expr):
        super(diag_vec, self).__init__(expr)

    def numeric(self, values):
        """Convert the vector constant into a diagonal matrix.
        """
        return np.diag(values[0])

    def shape_from_args(self):
        """A square matrix.
        """
        rows = self.args[0].shape[0]
        return (rows, rows)

    def is_symmetric(self):
        """Is the expression symmetric?
        """
        return True

    def is_hermitian(self):
        """Is the expression symmetric?
        """
        return True

    @staticmethod
    def graph_implementation(arg_objs, shape, data=None):
        """Convolve two vectors.

        Parameters
        ----------
        arg_objs : list
            LinExpr for each argument.
        shape : tuple
            The shape of the resulting expression.
        data :
            Additional data required by the atom.

        Returns
        -------
        tuple
            (LinOp for objective, list of constraints)
        """
        return (lu.diag_vec(arg_objs[0]), [])


class diag_mat(AffAtom):
    """Extracts the diagonal from a square matrix.
    """

    def __init__(self, expr):
        super(diag_mat, self).__init__(expr)

    @AffAtom.numpy_numeric
    def numeric(self, values):
        """Extract the diagonal from a square matrix constant.
        """
        # The return type in numpy versions < 1.10 was ndarray.
        v = np.diag(values[0])
        if isinstance(v, np.matrix):
            v = v.A[0]
        return v

    def shape_from_args(self):
        """A column vector.
        """
        rows, _ = self.args[0].shape
        return (rows,)

    @staticmethod
    def graph_implementation(arg_objs, shape, data=None):
        """Extracts the diagonal of a matrix.

        Parameters
        ----------
        arg_objs : list
            LinExpr for each argument.
        shape : tuple
            The shape of the resulting expression.
        data :
            Additional data required by the atom.

        Returns
        -------
        tuple
            (LinOp for objective, list of constraints)
        """
        return (lu.diag_mat(arg_objs[0]), [])
