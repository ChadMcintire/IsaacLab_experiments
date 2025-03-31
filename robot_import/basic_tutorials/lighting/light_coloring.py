# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""This script demonstrates how to spawn prims into the scene.

.. code-block:: bash

    # Usage
    ./isaaclab.sh -p scripts/tutorials/00_sim/spawn_prims.py

"""

"""Launch Isaac Sim Simulator first."""


import argparse

from isaaclab.app import AppLauncher

# create argparser
parser = argparse.ArgumentParser(description="Tutorial on spawning prims into the scene.")
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()
# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import isaacsim.core.utils.prims as prim_utils

import isaaclab.sim as sim_utils
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

from utils.quat import quaternion_from_degrees

def design_scene():
    """Designs the scene by spawning ground plane, light, objects and meshes from usd files."""
    # spawn distant light
    #cfg_light_distant = sim_utils.DistantLightCfg(
    #    intensity=500.0,
    #    color=(1.0, 0.0, 0.0),
    #)
    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))

    #Ground-plane
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)


    #Spawn in 3 cylinder lights, red, green, and blue
    #add red light
    cfg_light = sim_utils.CylinderLightCfg(intensity=3000.0, color=(1.0, 0.0, 0.0), length=5,)
    cfg_light.func("/World/Light", cfg_light, translation=(0.0, 1.0, 1.5))#, 

    #add green light
    cfg_light2 = sim_utils.CylinderLightCfg(intensity=3000.0, color=(0.0, 1.0, 0.0), length=5,)
    cfg_light2.func("/World/Light2", cfg_light2, translation=(0.0, -1.0, 1.5),  )

    #add blue light
    cfg_light2 = sim_utils.CylinderLightCfg(intensity=3000.0, color=(0.0, 0.0, 1.0), length=5,)
    cfg_light2.func("/World/Light3", cfg_light2, translation=(0.0, 3.0, 1.5),  )


    # translation (x,y,z)
    # orientation (w, x, y, z) (each float in x, y, z is 0 to 180, where w is a scalar component)
    # scale :    isaaclab.sim.spawners.lights.spawn_light has no attribute scale, but it does in isaac_sim, how do I access it or why can I not?


    # these are the same out put in isaacsim but both are not in the correct orientation
    #cfg_light.func("/World/Light", cfg_light, translation=(0.0, 0.0, 1.5),  orientation=(quaternion_from_degrees( 18, 18, 18)))#, orientation=(0.0,0.0,1.5),) #scale=(1.0, 2.0, 1.0))
    #cfg_light.func("/World/Light", cfg_light, translation=(0.0, 0.0, 1.5),  orientation=(0.888, 0.0, −0.325, 0.325))#, orientation=(0.0,0.0,1.5),) #scale=(1.0, 2.0, 1.0))

    #cfg_light.func("/World/Light", cfg_light, translation=(0.0, 0.0, 1.5),  orientation=(quaternion_from_degrees( 18, 18, 18)))#, orientation=(0.0,0.0,1.5),) #scale=(1.0, 2.0, 1.0))



def main():
    """Main function."""

    # Initialize the simulation context
    sim_cfg = sim_utils.SimulationCfg(dt=0.01, device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    # Set main camera
    sim.set_camera_view([2.0, 0.0, 2.5], [-0.5, 0.0, 0.5])

    # Design scene by adding assets to it
    design_scene()

    # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")

    # Simulate physics
    while simulation_app.is_running():
        # perform step
        sim.step()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
