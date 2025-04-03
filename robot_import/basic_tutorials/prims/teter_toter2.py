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

import isaaclab.sim as sim_utils
from isaaclab.sim import SimulationContext

import isaacsim.core.utils.prims as prim_utils
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
import isaaclab.utils.math as math_utils
from isaaclab.assets import RigidObject, RigidObjectCfg
import torch

def design_scene():
    """Designs the scene by spawning ground plane, light, objects and meshes from usd files."""
    # Ground-plane
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)

    # spawn distant light
    cfg_light_distant = sim_utils.DistantLightCfg(
        intensity=3000.0,
        color=(0.75, 0.75, 0.75),
    )
    cfg_light_distant.func("/World/lightDistant", cfg_light_distant, translation=(1, 0, 10))


    # Create Xform for the teter toter
    prim_utils.create_prim(f"/World/TeterToter", "Xform", translation= [0.0, 0.0, 0.0])

    # Make the base of the teter toter
    cube_Base_cfg = RigidObjectCfg(
        prim_path="/World/TeterToter/Base",
        spawn=sim_utils.CuboidCfg(
            size=[0.5,0.3,0.6],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(2.0, 0.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(),
    )
    base_object = RigidObject(cfg=cube_Base_cfg)

    # Make the seat of the teter toter
    cube_Seat_cfg = RigidObjectCfg(
        prim_path="/World/TeterToter/Seat",
        spawn=sim_utils.CuboidCfg(
            size=[0.4,3.8,0.2],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(2.0, 0.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg( pos=(0.0, 0.0, 0.9)),
    )
    seat_object = RigidObject(cfg=cube_Seat_cfg)

    # Make the right cube to bounce
    cube_right_cfg = RigidObjectCfg(
        prim_path="/World/TeterToter/Cube_right",
        spawn=sim_utils.CuboidCfg(
            size=[0.4,0.8,0.2],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 2.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg( pos=(0.0, 1.4, 1.9)),
    )
    right_cube_object = RigidObject(cfg=cube_right_cfg)

    # Make the left cube to bounce
    cube_left_cfg = RigidObjectCfg(
        prim_path="/World/TeterToter/Cube_left",
        spawn=sim_utils.CuboidCfg(
            size=[0.4,0.8,0.2],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 2.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg( pos=(0.0, -1.4, 300.9)),
    )
    left_cube_object = RigidObject(cfg=cube_left_cfg)


    #set up the scene
    scene_entities = {"base": base_object, "seat": seat_object, "right_cube": right_cube_object, "left_cube": left_cube_object}
    return scene_entities


    
def run_simulator(sim: sim_utils.SimulationContext, entities: dict[str, RigidObject], origins: torch.Tensor):
    """Runs the simulation loop."""
    sim_dt = sim.get_physics_dt() 

    ## Simulate physics
    while simulation_app.is_running():
        sim.step()


def main():
    """Main function."""
    # Load kit helper
    
    # if the brick is above a value of 30, the collisions do not occur
    # we can either slow down the simulation by changing the dt in the SimulationCfg
    # or by passing in the enable_ccd=True to the PhysxCfg, (CCD stands for 
    # continuous collision detection

    physx = sim_utils.PhysxCfg(enable_ccd=True)
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device, physx=physx)
    #sim_cfg = sim_utils.SimulationCfg(dt=0.005, device=args_cli.device, physx=physx)
    sim = SimulationContext(sim_cfg)

    # The eye is where the camera actually is, the target is what you want the camera to 
    # look at

    # Alternate camera angles
    #sim.set_camera_view(eye=[1.5, 0.0, 1.0], target=[0.0, 0.0, 0.0])
    #sim.set_camera_view(eye=[10.0, 0.0, 3.0], target=[0.0, 0.0, 0.0])

    sim.set_camera_view(eye=[-35.0, .0, 30.0], target=[0.0, 0.0, 0.0])
    # Design scene
    scene_entities = design_scene()
    # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")
    # Run the simulator
    run_simulator(sim, scene_entities, {})


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
