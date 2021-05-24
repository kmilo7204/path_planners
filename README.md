# Path Planners
This repository contains the implementation of different algorithms for path planning (In discrete and continuous time). Most of the projects are developed in **python** and **pygame** for simplicity (It is better to read Python) as this repository intends to be a base for different projects.
 
Grid-based algorithms
* Dijkstra's 
* A*

<div align="center"><img src="https://user-images.githubusercontent.com/49252525/119419636-545c2600-bcc0-11eb-81ec-b30373f3ec96.gif" width="40%" height="40%"/></div>

## Usage
In order to use this "game" you need to follow the instructions provided below once you have run the main script. Run the script named as the algorithm you want to test (i.e. a_star.py will execute a search based on A*)

* **First click:** Select the start location within the grid.
* **Second click:** Select the final location within the grid.
* **Third and following clicks:** Allocate obstacles inside the grid; however, if you click and obstacle it will be removed from the grid.
* **Spacebar:** Start the search

## Setting up the virtual environment
Anaconda or Minicoda is required for this project as you must create a conda environment with the required dependencies.

### Create the environment
For creating the environment use the following bash command.
```bash
conda env create -f environment.yml
```

Check if the environment was successfully created (planners_env should be listed when running the command below)
```bash
conda env list
```

### Activate the environment
For activating the environment use the following bash command (Use the Ananconda Prompt if not recognized)
```bash
conda activate planners_env
```
