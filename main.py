import numpy as np

from local_maps import LocalMapsforPeriodicGrid
from periodic_grid import PeriodicGrid
from ips import IPSonPeriodicGrid
from simulation import simulate


if __name__ == "__main__":

    

    # -------------------------------------------------------------------------
    # Voter Model
    # Each cell copies the state of one of its 4 neighbors (up/down/left/right)
    # at a given rate. Over time, the grid converges to consensus.
    # -------------------------------------------------------------------------
    # --- Grid configuration ---
    grid_size = 50
    dimension = 2
    colors = 3
    grid_voter = PeriodicGrid(colors=colors, dimension=dimension, size=grid_size)

    # --- Local maps ---
    rate = 1.5

    # One local map per direction: cell at (0,0) copies its neighbor
    voter_right = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(0, 1)],
        transition_rule=lambda x: [x[0]], rate=rate
    )
    voter_up = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(1, 0)],
        transition_rule=lambda x: [x[0]], rate=rate
    )
    voter_left = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(0, -1)],
        transition_rule=lambda x: [x[0]], rate=rate
    )
    voter_down = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(-1, 0)],
        transition_rule=lambda x: [x[0]], rate=rate
    )
    # --- set up IPS ---
    ips_voter = IPSonPeriodicGrid(
        current_grid=grid_voter,
        local_maps_list=[voter_right, voter_up, voter_left, voter_down],
        end_time=100.0,
        dt=0.1
    )
    
    # --- Run simulation ---
    simulate(ips_voter, ms=0.01, time_steps=10)

    

     # -------------------------------------------------------------------------
    # Contact Process
    # Models infection spread: active cells (state=1) can infect neighbors
    # (branching), and spontaneously recover (death).
    # -------------------------------------------------------------------------
    # --- Grid configuration ---

    # Initialize a blank grid and place a small vertical stripe of active cells
    # at the center as the starting configuration
    arr = np.full((grid_size, grid_size), 0)
    arr[grid_size // 2,     grid_size // 2] = 1
    arr[grid_size // 2 + 1, grid_size // 2] = 1
    arr[grid_size // 2 - 1, grid_size // 2] = 1

    grid_contact = PeriodicGrid.from_array(arr)


    # --- Local maps ---

    # Branching: a cell spreads its state to a neighbor if it is active
    rate_branching = 0.2
    bra_right = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(0, 0), (0, 1)],
        transition_rule=lambda x: [max(x)], rate=rate_branching
    )
    bra_up = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(0, 0), (1, 0)],
        transition_rule=lambda x: [max(x)], rate=rate_branching
    )
    bra_down = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(0, 0), (0, -1)],
        transition_rule=lambda x: [max(x)], rate=rate_branching
    )
    bra_left = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[(0, 0), (-1, 0)],
        transition_rule=lambda x: [max(x)], rate=rate_branching
    )

    # Death: a cell spontaneously returns to state 0 regardless of neighbors
    rate_death = 0.1
    death = LocalMapsforPeriodicGrid.with_constant_rate(
        grid_size=grid_size, dimension=dimension,
        rel_cells_to_change=[(0, 0)], rel_influencing_cells=[],
        transition_rule=lambda _: [0], rate=rate_death
    )
    
    # --- set up IPS ---
    ips_contact = IPSonPeriodicGrid(
        current_grid=grid_contact,
        local_maps_list=[bra_right, bra_up, bra_down, bra_left, death],
        end_time=100.0,
        dt=0.1
    )

    # --- Run simulation ---
    simulate(ips_contact, ms=0.01, time_steps=10)
    
