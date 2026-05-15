import numpy as np


class PeriodicGrid():
    """
    Represents a periodic grid with a defined number of colors/states, dimensions, and size.
    """

    def __init__(self, colors: int, dimension: int, size: int, grid = None) -> None:
        """
        Initializes the grid.

        :param colors:    Number of possible states/colors per cell.
        :param dimension: Dimensionality of the grid (allowed: 1, 2, or 3).
        :param size:      Side length of the grid (equal in every dimension).
        :param grid:      Optional predefined NumPy array. Randomly generated
                          if not provided.
        """
        # Dimension must be 1, 2, or 3 — raise an error otherwise
        if dimension < 1 or dimension > 3:
            raise ValueError("Dimension must be 1, 2 or 3.")

        self.colors = colors        # Number of states/colors
        self.dimension = dimension  # Dimensionality of the grid
        self.size = size            # Side length of the grid

        if grid is None:
            # No grid provided → generate a random grid with integer values
            # in the range [0, colors) and shape (size x size x ...)
            self.grid = np.random.randint(colors, size=(size,) * dimension)
        else:
            # Validate that the provided grid has the expected shape
            if grid.shape != (size,) * dimension:
                raise ValueError(f"Grid shape must be {(size,) * dimension}")
            self.grid = grid

    @classmethod
    def from_array(cls, grid: np.ndarray):
        """
        Creates a PeriodicGrid instance directly from an existing NumPy array.
        Grid properties (colors, dimension, size) are derived automatically
        from the array.

        :param grid: NumPy array with a square/cubic shape.
        :return:     New PeriodicGrid instance.
        """
        # Ensure the array has equal size along every axis
        # (e.g. 5x5, 5x5x5 — but not 5x3)
        if grid.shape != (grid.shape[0],) * len(grid.shape):
            raise ValueError("Grid shape has wrong dimensions.")

        # Number of colors is derived from the highest value in the array + 1
        # (since states are indexed from 0 to max)
        return cls(
            colors=np.max(grid) + 1,
            dimension=len(grid.shape),  # Number of axes = dimensionality
            size=grid.shape[0],         # Side length (equal across all dimensions)
            grid=grid
        )