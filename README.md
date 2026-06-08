# IPS Simulator

A Python framework for simulating **Interacting Particle Systems (IPS)** on periodic grids.

## Overview

An IPS is a stochastic process where cells on a grid update their states based on the states of their neighbors. This project provides a flexible, composable framework to define and simulate such systems in 1D, 2D, or 3D.

**Implemented example models:**
- **Voter Model** — each cell randomly copies a neighbor's state; the grid converges to consensus over time
- **Contact Process** — active cells spread to neighbors (branching) and spontaneously recover (death); models epidemic spread

## Project Structure

```
├── periodic_grid.py   # PeriodicGrid: n-dimensional periodic grid with random or custom initialization
├── local_maps.py      # LocalMapsforPeriodicGrid: stochastic local transition rules
├── ips.py             # IPSonPeriodicGrid: orchestrates the simulation by applying local maps over time
├── simulation.py      # Visualization via matplotlib animations (2D implemented)
└── main.py            # Example simulations: Voter Model and Contact Process
```

## Requirements

- Python 3.10+
- numpy>=1.24
- matplotlib>=3.7

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

Run the example simulations directly:
```bash
python main.py
```

Or define your own IPS:
```python
from periodic_grid import PeriodicGrid
from local_maps import LocalMapsforPeriodicGrid
from ips import IPSonPeriodicGrid
from simulation import simulate

# Create a random 2D grid with 2 states
grid = PeriodicGrid(colors=2, dimension=2, size=50)

# Define a rule: each cell copies its right neighbor
rule = LocalMapsforPeriodicGrid.with_constant_rate(
    grid_size=50, dimension=2,
    rel_cells_to_change=[(0, 0)],
    rel_influencing_cells=[(0, 1)],
    transition_rule=lambda x: [x[0]],
    rate=1.0
)

# Set up and run the simulation
ips = IPSonPeriodicGrid(current_grid=grid, local_maps_list=[rule], end_time=50.0, dt=0.1)
simulate(ips, ms=10, time_steps=5)
```

## TODOs

- **Create video files from simulation**(`main.py`): Create video files from the simulations, as an example case
- **Simultaneous local map application** (`ips.py`): local maps are currently applied sequentially within each time step. They should be applied simultaneously — all reading from the same grid snapshot — to avoid order-dependent artifacts.
- **1D visualization** (`simulation.py`): not yet implemented. Planned as a space-time diagram (rows = time, columns = cell index).
- **3D visualization** (`simulation.py`): not yet implemented.

## License

MIT
