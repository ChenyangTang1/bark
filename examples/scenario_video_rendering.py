# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# ffmpeg must be installed and available on command line


from modules.runtime.scenario.scenario_generation.uniform_vehicle_distribution import UniformVehicleDistribution
from modules.runtime.commons.parameters import ParameterServer
from modules.runtime.runtime import Runtime
from modules.runtime.viewer.matplotlib_viewer import MPViewer
from modules.runtime.viewer.video_renderer import VideoRenderer
import os

scenario_param_file ="highway_merging.json" # must be within examples params folder
param_server = ParameterServer(filename= os.path.join("examples/params/",scenario_param_file))
scenario_generation = UniformVehicleDistribution(num_scenarios=10, random_seed=0, params=param_server)

viewer = MPViewer(params=param_server, x_range=[5060, 5160], y_range=[5070,5150])
sim_step_time = param_server["simulation"]["step_time",
                                           "Step-time used in simulation",
                                           0.2]
sim_real_time_factor = param_server["simulation"]["real_time_factor",
                                                  "execution in real-time or faster", 1]
scenario, idx = scenario_generation.get_next_scenario()


# Rendering WITHOUT intermediate steps
video_renderer = VideoRenderer(renderer=viewer, world_step_time=sim_step_time)
env = Runtime(0.2,
              video_renderer,
              scenario_generation,
              render=True)
env.reset()
for _ in range(0, 5):
  env.step()  
video_renderer.export_video(filename="examples/scenarios/test_video_step")

# Rendering WITH intermediate steps
video_renderer = VideoRenderer(renderer=viewer, world_step_time=sim_step_time, render_intermediate_steps=10)
env = Runtime(0.2,
              video_renderer,
              scenario_generation,
              render=True)
env.reset()
for _ in range(0, 5):
  env.step()  

video_renderer.export_video(filename="examples/scenarios/test_video_intermediate")
