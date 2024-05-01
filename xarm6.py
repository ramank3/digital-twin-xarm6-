import pybullet as p
import pybullet_data
import numpy as np
import csv
import time
import socket
import json
# Initialize the PyBullet simulation
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load the URDF file
table_urdf_file = "C:\\Users\\rpk5375\\PycharmProjects\\pythonProject2\\gym-xarm\\gym_xarm\\envs\\urdf\\my_table.urdf"
robot_id = p.loadURDF(table_urdf_file,[0, 0, -0.625], useFixedBase=True)
arm_urdf = "C:\\Users\\rpk5375\\bullet3\examples\pybullet\gym\pybullet_data\\xarm\\xarm6_robot.urdf"
robotic_arm = p.loadURDF(arm_urdf, [0, 0, 0], useFixedBase=True)

# Generate random base position for the Lego block within a specified range
x_range = [-0.3, 0.3]  # Adjust the X range as needed
y_range = [-0.3, 0.3]  # Adjust the Y range as needed
z_height = 0.025  # Adjust the height as needed

cube_base_pos = [np.random.uniform(*x_range), np.random.uniform(*y_range), z_height]
lego_base_pos = [np.random.uniform(*x_range), np.random.uniform(*y_range), z_height]
sphere_base_pos = [np.random.uniform(*x_range), np.random.uniform(*y_range), z_height]

cube_urdf = "C:\\Users\\rpk5375\\PycharmProjects\\pythonProject2\\gym-xarm\\gym_xarm\\envs\\urdf\\my_cube.urdf"
sphere_urdf = "C:\\Users\\rpk5375\\PycharmProjects\\pythonProject2\\gym-xarm\\gym_xarm\\envs\\urdf\\my_sphere.urdf"
lego_urdf = "C:\\Users\\rpk5375\\PycharmProjects\\pythonProject2\\gym-xarm\\gym_xarm\\envs\\urdf\\my_lego.urdf"
cube = p.loadURDF(cube_urdf,cube_base_pos, useFixedBase=False)
lg_v = p.loadURDF(lego_urdf,lego_base_pos, useFixedBase=False)
sphere = p.loadURDF(sphere_urdf,sphere_base_pos, useFixedBase=False)

def set_joint_angles(joint_data):
    for i, angle in enumerate(joint_data):
        target_joint_index = i +1  # Adjust index so that it targets joint 3
        if target_joint_index < p.getNumJoints(robotic_arm):  # Ensure index is within range
            p.setJointMotorControl2(bodyUniqueId=robotic_arm,
                                    jointIndex=target_joint_index,
                                    controlMode=p.POSITION_CONTROL,
                                    targetPosition=angle)
# Setup for the socket server
HOST = '127.0.0.1'
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
conn, addr = server_socket.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        joint_angles = json.loads(data.decode('utf-8'))
        set_joint_angles(joint_angles)
        p.stepSimulation()
        time.sleep(0.001)  # Adjust as needed for simulation timing

p.disconnect()

# asynchronous connection
'''with open('C:\\Users\\rpk5375\\Downloads\\xArm-Python-SDK-master\\xArm-Python-SDK-master\\example\\wrapper\\common\\xarm_data4.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        joint_angles = [float(angle) for angle in row[1:]]  # Assuming first column is timestamp
        set_joint_angles(joint_angles)
        time.sleep(.4)  # Adjust based on your data's timestamp
        p.stepSimulation()
p.disconnect()'''