import numpy as np

from local_maps import LocalMapsforPeriodicGrid
from periodic_grid import PeriodicGrid


class IPSonPeriodicGrid:
    """
    Represents an Interacting Particle System (IPS) on a periodic grid.

    Holds a list of local transition rules (LocalMapsforPeriodicGrid) that
    are applied sequentially at each time step. The grid evolves by repeatedly
    calling each local map's apply() method, which stochastically updates
    cell states based on their neighborhoods.

    FIXME: Currently, local maps are applied sequentially within each time step.
    """

    def __init__(
        self,
        current_grid: PeriodicGrid,
        local_maps_list: list[LocalMapsforPeriodicGrid],
        dt: float,
        end_time: float
    ) -> None:
        """
        Initializes the IPS simulation.

        :param current_grid:    The current periodic grid state to evolve.
        :param local_maps_list: Ordered list of local transition rules to apply
                                at each time step. Rules are applied sequentially,
                                so their order may affect the simulation outcome.
        :param dt:              Length of each time step. Should be small enough
                                that rate * dt << 1 for all cells and rules.
        :param end_time:        Total simulation time (not directly used for
                                stepping here, but stored for reference or
                                external control).
        """
        self.local_maps_list = local_maps_list  # Transition rules applied each step
        self.dt = dt                            # Time step size
        self.current_grid = current_grid        # Current state of the periodic grid
        self.end_time = end_time                # Total intended simulation time

    def timesteps(self, num_steps: int) -> None:
        """
        Advances the simulation by a given number of time steps.

        At each step, every local map in local_maps_list is applied in order
        to the grid. After all steps are complete, the result is written back
        to the PeriodicGrid object.

        :param num_steps: Number of time steps to simulate.
        """
        # Work directly on the raw NumPy array for performance
        grid = self.current_grid.grid

        for _ in range(num_steps):
            # FIXME: Local maps are currently applied sequentially, meaning each
            # rule sees the grid state already modified by the previous one within
            # the same time step. They should instead be applied simultaneously —
            # i.e. all rules read from the same snapshot of the grid and their
            # updates are merged afterwards. This may require collecting all
            # proposed changes first and resolving conflicts before writing them back.
            for local_maps in self.local_maps_list:
                local_maps.apply(grid, self.dt)

        # Write the evolved grid back to the PeriodicGrid wrapper object
        self.current_grid.grid = grid
