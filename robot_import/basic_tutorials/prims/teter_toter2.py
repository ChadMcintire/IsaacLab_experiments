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
from isaaclab.sim import SimulationContext
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

        # Create separate groups called "Origin1", "Origin2", "Origin3"
    # Each group will have a robot in it
    origins = [[0.25, 0.25, 0.0], [-0.25, 0.25, 0.0], [0.25, -0.25, 0.0], [-0.25, -0.25, 0.0]]
    for i, origin in enumerate(origins):
        prim_utils.create_prim(f"/World/Origin{i}", "Xform", translation=origin)

    # Rigid Object
    cone_cfg = RigidObjectCfg(
        prim_path="/World/Origin.*/Cone",
        spawn=sim_utils.ConeCfg(
            radius=0.1,
            height=0.2,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 1.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(),
    )
    cone_object = RigidObject(cfg=cone_cfg)


    prim_utils.create_prim(f"/World/TeterToter", "Xform", translation= [0.0, 0.0, 0.0])
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
        # 0.29562, 0.1963, -0.24517
    )
    seat_object = RigidObject(cfg=cube_Seat_cfg)


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
        # 0.29562, 0.1963, -0.24517
    )
    right_cube_object = RigidObject(cfg=cube_right_cfg)


    #prim_utils.create_prim(f"/World/TeterToter", "Xform", translation= [0.0, 0.0, 2.0])
    cube_left_cfg = RigidObjectCfg(
        prim_path="/World/TeterToter/Cube_left",
        spawn=sim_utils.CuboidCfg(
            size=[0.4,0.8,0.2],
            rigid_props=sim_utils.RigidBodyPropertiesCfg(),
            mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 2.0, 0.0), metallic=0.2),
        ),
        init_state=RigidObjectCfg.InitialStateCfg( pos=(0.0, -1.4, 200.9)),
        # 0.29562, 0.1963, -0.24517
    )
    left_cube_object = RigidObject(cfg=cube_left_cfg)



    # return the scene information
    #scene_entities = {"cone": cone_object, "base": base_object}#, "seat": seat_object}
    scene_entities = {"cone": cone_object, "base": base_object, "seat": seat_object, "right_cube": right_cube_object, "left_cube": left_cube_object}
    return scene_entities, origins


    
def run_simulator(sim: sim_utils.SimulationContext, entities: dict[str, RigidObject], origins: torch.Tensor):
    """Runs the simulation loop."""
    # Extract scene entities
    # note: we only do this here for readability. In general, it is better to access the entities directly from
    #   the dictionary. This dictionary is replaced by the InteractiveScene class in the next tutorial.
    cone_object = entities["cone"]
    # Define simulation stepping
    sim_dt = sim.get_physics_dt() 
    #new_dt = sim_dt * 0.5  # Slow down simulation by 50%

    #sim.set_physics_dt(new_dt)  # Apply the new timeste
    #print(f"Updated physics timestep: {new_dt}")

    sim_time = 0.0
    count = 0
    ## Simulate physics
    while simulation_app.is_running():
    #    # reset
    #    if count % 250 == 0:
    #        # reset counters
    #        sim_time = 0.0
    #        count = 0
    #        # reset root state
    #        root_state = cone_object.data.default_root_state.clone()
    #        # sample a random position on a cylinder around the origins
    #        root_state[:, :3] += origins
    #        root_state[:, :3] += math_utils.sample_cylinder(
    #            radius=0.1, h_range=(0.25, 0.5), size=cone_object.num_instances, device=cone_object.device
    #        )
    #        # write root state to simulation
    #        cone_object.write_root_pose_to_sim(root_state[:, :7])
    #        cone_object.write_root_velocity_to_sim(root_state[:, 7:])
    #        # reset buffers
    #        cone_object.reset()
    #        print("----------------------------------------")
    #        print("[INFO]: Resetting object state...")
    #    # apply sim data
        cone_object.write_data_to_sim()
        # perform step
        sim.step()
        # update sim-time
        sim_time += sim_dt
        count += 1
        # update buffers
        cone_object.update(sim_dt)
        # print the root position
        if count % 50 == 0:
            print(f"Root position (in world): {cone_object.data.root_state_w[:, :3]}")


def main():
    """Main function."""
    # Load kit helper
    physx = sim_utils.PhysxCfg(enable_ccd=True)
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device, physx=physx)
    #sim_cfg = sim_utils.SimulationCfg(dt=0.005, device=args_cli.device, physx=physx)
    #sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = SimulationContext(sim_cfg)



    # Set main camera
    #sim.set_camera_view(eye=[1.5, 0.0, 1.0], target=[0.0, 0.0, 0.0])
    #sim.set_camera_view(eye=[10.0, 0.0, 3.0], target=[0.0, 0.0, 0.0])
    sim.set_camera_view(eye=[-35.0, .0, 30.0], target=[0.0, 0.0, 0.0])
    # Design scene
    scene_entities, scene_origins = design_scene()
    scene_origins = torch.tensor(scene_origins, device=sim.device)
    # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")
    # Run the simulator
    run_simulator(sim, scene_entities, scene_origins)


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
