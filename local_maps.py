
from typing import Callable
import numpy as np


class LocalMapsforPeriodicGrid():
    """
    Represents a stochastic cellular automaton on a periodic grid.

    Each cell can act as a reference point that triggers a local transition:
    it reads values from a set of neighboring cells (influencing positions),
    applies a transition rule, and writes the results to another set of
    neighboring cells (positions to change).

    Transitions are stochastic — each cell fires independently with a
    probability proportional to its rate and the time step dt.
    """

    def __init__(
        self,
        grid_size: int,
        dimension: int,
        rel_cells_to_change: list[tuple[int, ...]],
        rel_influencing_cells: list[tuple[int, ...]],
        transition_rule: Callable[[list[int]], list[int]],
        rates: np.ndarray
    ) -> None:
        """
        Initializes the LocalMapsGrid.

        :param grid_size:               Side length of the grid (equal in every dimension).
        :param dimension:               Dimensionality of the grid (1, 2, or 3).
        :param rel_cells_to_change:     List of relative coordinates (offsets from the
                                        reference cell) whose values will be overwritten
                                        by the transition rule's output.
        :param rel_influencing_cells: List of relative coordinates (offsets from the
                                          reference cell) whose current values are passed
                                          as input to the transition rule.
        :param transition_rule:         Function mapping a list of input cell states to a
                                        list of output cell states.
        :param rates:                   Array of per-cell firing rates, shaped
                                        (grid_size,) * dimension. Higher rate = higher
                                        probability of firing per unit time.
        """
        # Dimension must be 1, 2, or 3
        if dimension < 1 or dimension > 3:
            raise ValueError("Dimension must be 1, 2 or 3.")

        # Every coordinate in both offset lists must match the grid's dimension
        for coord in rel_cells_to_change + rel_influencing_cells:
            if len(coord) != dimension:
                raise ValueError("All coordinates must have the same dimension as the grid.")

        # The rates array must match the grid shape exactly
        if rates.shape != (grid_size,) * dimension:
            raise ValueError(f"Rates must have shape {(grid_size,) * dimension}")

        self.grid_size = grid_size
        self.dimension = dimension
        self.rel_cells_to_change = rel_cells_to_change              # Neighbouring cells of reference cell that get updated
        self.rel_influencing_cells = rel_influencing_cells          # Neighbouring cells of reference cell that influence the update 
        self.transition_rule = transition_rule                      # State update function
        self.rates = rates                                          # Per-cell firing rates

    @classmethod
    def with_constant_rate(
        cls,
        grid_size: int,
        dimension: int,
        rel_cells_to_change: list[tuple[int, ...]],
        rel_influencing_cells: list[tuple[int, ...]],
        transition_rule: Callable[[list[int]], list[int]],
        rate: float
    ):
        """
        Convenience constructor that assigns the same firing rate to every cell.

        :param rate: Uniform firing rate applied to all cells.
        :return:     A new LocalMapsGrid instance with a constant rate array.
        """
        # Fill the entire rate array with the same scalar value
        rates = np.full((grid_size,) * dimension, rate)
        return cls(grid_size, dimension, rel_cells_to_change, rel_influencing_cells, transition_rule, rates)

    def apply(self, grid: np.ndarray, dt: float) -> None:
        """
        Advances the grid by one time step of length dt.

        For each cell, a Poisson-style firing check is performed:
        the cell fires if a uniform random value falls below rate * dt.
        All firing cells are collected first, then their transition rules are
        applied simultaneously to avoid order-dependent artifacts.

        :param grid: The current grid state (modified in-place).
        :param dt:   Length of the time step. Larger dt → more firings on average.
        """
        # Work on a copy so all transitions within one step are based on the
        # same snapshot of the grid (synchronous update)
        new_grid = np.copy(grid)

        # Determine which cells fire this time step:
        # draw uniform random values for every cell and compare to rate * dt.
        # np.argwhere returns an array of coordinates where the condition is True.
        ref_positions = np.argwhere(np.random.rand(*self.rates.shape) < self.rates * dt)

        grid_shape = (self.grid_size,) * self.dimension

        for ref_position in ref_positions:
            # Collect the current states of all influencing neighbors.
            # The modulo ensures periodic boundary conditions.
            input_values = [
                int(grid[tuple((ref_position + rel_pos) % grid_shape)])
                for rel_pos in self.rel_influencing_cells
            ]

            # Apply the transition rule to get the new output states
            output_values = self.transition_rule(input_values)

            # Write each output value to its corresponding target cell,
            # again using modulo for periodic boundaries
            for rel_pos, new_value in zip(self.rel_cells_to_change, output_values):
                position = (ref_position + rel_pos) % grid_shape
                new_grid[tuple(position)] = new_value

        # Overwrite the original grid in-place with the updated copy
        grid[:] = new_grid