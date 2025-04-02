import numpy as np
from scipy.spatial.transform import Rotation as R

np.set_printoptions(precision=17, threshold=10, suppress=True, )

def quaternion_from_degrees(roll, pitch, yaw):
  """
  Converts Euler angles (roll, pitch, yaw) in degrees to a quaternion.

  Args:
    roll: Rotation around the x-axis in degrees.
    pitch: Rotation around the y-axis in degrees.
    yaw: Rotation around the z-axis in degrees.

  Returns:
    A NumPy array representing the quaternion (w, x, y, z).
  """
  print("Roll, pitch, yaw", roll, pitch, yaw)
  # Create a rotation object from Euler angles
  rotation = R.from_euler('xyz', [roll, pitch, yaw], degrees=True)

  # Get the quaternion representation
  quaternion = rotation.as_quat()

  #change the last element "w" to be first so we have "wxyz" 
  quaternion_wxyz = np.concatenate(([quaternion[-1]], quaternion[:-1]))

  # format needs to be a tuple 
  quat_as_tup = tuple(quaternion_wxyz)

  #original_cordinate = R.from_quat(np.around(quaternion, decimals=10)).as_euler('xyz', degrees=True)
  print("original, original_cordinate", original_cordinate)

  return tuple( np.around(quat_as_tup , decimals=10))

#quaternion_from_degrees(-163, -35, -153)
