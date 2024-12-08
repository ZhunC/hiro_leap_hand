# Hiro Leap Hand
This repo contains the two necessary ROS (Noetic) packages for controlling the Leap hand with the Stretchsense glove. 

## Installation
1. Go to the `src` folder of your ROS Noetic workspace.
2. Clone this repo:
```bash
git clone [https://github.com/username/repo.git](https://github.com/ZhunC/hiro_leap_hand.git)
```
3. Move the packages under `src` directly:
```bash
mv hiro_leap_hand/ros_module .
mv hiro_leap_hand/stretchSenseROS .
rm -rf hiro_leap_hand
```
4. Now make sure all dependencies are installed for both packages:
```bash
# optional virtual environment
cd ..
python -m venv leap_hand_env
source leap_hand_env/bin/activate

# dependencies of Leap Hand interface
cd src/ros_module
pip install dynamixel_sdk numpy

# dependencies of StretchSense glove
cd ../stretchSenseROS
pip install -r requirements.txt
```
5. Now go back to the workspace's root folder and run `catkin_make`
6. Set up bashrc and source:
```bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
7. Finally, set up executables:
```bash
cd src/ros_module
chmod +x leaphand_node.py
```
You're all set! 

## Using the hand
```bash
# 1. Run roscore
roscore

# 2. In a separate terminal, run the Rviz Visualizer. Choose one depending on which hand it is.
roslaunch stretchsense smartGloveModelLeft.launch
# or
roslaunch stretchsense smartGloveModelRight.launch

# 3. In a separate terminal, run the glove's main script. Follow the console instructions to input:
# name, id of glove, right/left.
# Afterwards, you'll have 5 seconds to open the Rviz window for calibration.
# During calibration, move your hand such that it has the same pose as shown in Rviz.
# Maintain the pose until it changes on Rviz; you'll know the calibration is finished once the simulated hand in Rviz starts moving along yours.
roslaunch stretchsense smartGloveApplication.launch

# 3.5 If the behavior of the simulated hand is satisfactory, you can move onto step 4.
# Otherwise, you can recalibrated by rerunning the above line.
# This time, after name, id, and r/l, you'll be prompted if recalibration is needed.
# Type 'y' if you want to; type 'n' if you want to just use the glove as it is.

# 4. In a separate terminal, connect the hand
cd <workspace path>/src/ros_module
roslaunch example.launch
```
Now the hand should be moving alongside the glove. 

## References
You can find the original repo here:
LEAP Hand: https://github.com/leap-hand/LEAP_Hand_API.git
Stretchsense glove interface: https://github.com/alvee1994/stretchSenseROS.git
