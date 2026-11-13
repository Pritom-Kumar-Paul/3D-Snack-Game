# 3D-Snack-Game
A classic Snake game in 3D built with Python, pygame and PyOpenGL. Rotate and zoom the camera freely with screen-relative controls.
# 🐍 3D Snake

A classic Snake game in 3D, written in **Python** with **pygame** and **PyOpenGL**.
Rotate and zoom the camera freely while you play. Controls always stay relative to your screen, no matter the camera angle. No external assets, everything is drawn with simple OpenGL cubes in a single file.


## Features

- Pure OpenGL 3D graphics (cubes, lighting, checkerboard floor, walls)
- Free camera: drag with the mouse to rotate, scroll to zoom
- Screen-relative controls, so "up" is always up on your screen even after rotating
- Snake speeds up as your score grows
- Bobbing food, gradient snake body, red snake on game over
- Single file, around 200 lines, easy to read and modify

## Installation

Requires Python 3.8+.

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
pip install pygame PyOpenGL
python snake_3d.py
```

## Controls

| Input | Action |
|-------|--------|
| Arrow keys / WASD | Move the snake (relative to the screen) |
| Mouse drag (left button) | Rotate the camera |
| Mouse scroll | Zoom in / out |
| R | Restart |
| ESC | Quit |

## How to play

- Eat the red cube to grow and score **1 point**.
- Hitting a wall or your own body ends the game.
- The snake gets faster with every point, down to a minimum step time of 70 ms.
- Score and status are shown in the window title.

## Tweak it

Constants at the top of `snake_3d.py`:

```python
GRID = 20        # board is GRID x GRID cells
STEP_MS = 140    # starting delay between snake moves (lower = faster)
```

## Ideas for the future

- [ ] Wrap-around walls mode
- [ ] Obstacles and bonus food
- [ ] Sound effects
- [ ] On-screen score display and high-score saving
- [ ] Snake that goes up and down (full 3D movement)

## Built with

- [Python](https://www.python.org/)
- [pygame](https://www.pygame.org/)
- [PyOpenGL](https://pyopengl.sourceforge.net/)

## License

MIT, see [LICENSE](LICENSE). Feel free to fork and build on it.
