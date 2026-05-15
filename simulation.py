import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from ips import IPSonPeriodicGrid
from periodic_grid import PeriodicGrid


def simulate(ips: IPSonPeriodicGrid, ms: float, time_steps: int) -> None:
    """
    Entry point for simulating an IPS.

    Dispatches to the appropriate dimension-specific simulation function
    based on the grid's dimensionality. Currently only 2D visualization
    is implemented.

    :param ips:        The IPS simulation object containing the grid and transition rules.
    :param ms:         Delay between animation frames in milliseconds.
    :param time_steps: Number of simulation steps to advance per animation frame.

    TODO: Implement 1D and 3D visualization methods. 
    """
    if ips.current_grid.dimension == 1:
        simulate_1d_grid(ips, ms, time_steps)
    elif ips.current_grid.dimension == 2:
        simulate_2d_grid(ips, ms, time_steps)
    elif ips.current_grid.dimension == 3:
        simulate_3d_grid(ips, ms, time_steps)


def simulate_1d_grid(ips: IPSonPeriodicGrid, ms: float, time_steps: int) -> None:
    """
    Visualizes a 1D periodic grid simulation.

    TODO: Not yet implemented. Should display the grid as a space-time diagram
    (rows = time, columns = cell index) to show the evolution over time.
    """
    pass


def simulate_2d_grid(ips: IPSonPeriodicGrid, ms: float, time_steps: int) -> None:
    """
    Visualizes a 2D periodic grid simulation as a real-time animated colormap.

    At each animation frame, the simulation is advanced by `time_steps` steps
    and the display is updated to reflect the new grid state.

    :param ips:        The IPS simulation object containing the grid and transition rules.
    :param ms:         Delay between animation frames in milliseconds.
    :param time_steps: Number of simulation steps to advance per animation frame.
    """
    fig, ax = plt.subplots()

    colors = ips.current_grid.colors

    # Display the initial grid state as a colormap;
    # vmin/vmax are fixed to the full color range to keep the colormap stable across frames
    im = ax.imshow(ips.current_grid.grid, cmap='viridis', vmin=0, vmax=colors - 1)

    # Add a text element to display the current simulation time
    frame_text = ax.text(
    0.5, -0.05, "",                # x, y in axes coordinates
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=12
    )

    # Save end_time, dt and time_steps for use in the animation update function
    end_time = ips.end_time
    dt = ips.dt

    def update(frame):
        """
        Animation callback: advances the simulation and refreshes the displayed grid.

        :param frame: Current frame index (provided by FuncAnimation, unused directly).
        :return:      List of updated artists for blitting.
        """
        # Advance the simulation by the specified number of time steps
        ips.timesteps(time_steps)

        # Update the colormap with the new grid state
        im.set_array(ips.current_grid.grid)

        # Update the frame text to show the current simulation time
        frame_text.set_text(f"Time: {frame * time_steps * dt:.2f}/ {end_time:.2f}")
        return [im, frame_text]

    # Total number of frames = total simulation time divided by a single time step
    frames = int(end_time / (dt * time_steps))

    anim = FuncAnimation(
        fig=fig,
        func=update,       # Called once per frame
        frames=frames,     # Total number of frames to render
        interval=ms,       # Milliseconds between frames
        blit=False,         # Full redraw each frame 
        repeat=False       # Do not loop the animation
    )

    plt.show()


def simulate_3d_grid(ips: IPSonPeriodicGrid, ms: float, time_steps: int) -> None:
    """
    Visualizes a 3D periodic grid simulation.

    TODO: Not yet implemented. Could use a volumetric renderer or display
    individual 2D slices of the 3D grid side by side or as a scrollable view.
    """
    pass