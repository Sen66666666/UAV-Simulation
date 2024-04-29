
wind_active = False # Select whether you want to activate wind or not
group_number = 10  # Enter your group number here

m=0.957122 # The mass of UAV
arm_length=0.25 # The arm length of UAV
uav_inertia= 0.35722 # The inertia of UAV
g=9.81 # The gravity acceleration

## Initialization of the integral term of the PID controller
integral_x=0 
integral_y=0
integral_attitude=0

def controller(state, target_pos, dt):
    # Refer to the integral term of the global variable
    global integral_x,integral_y,integral_attitude

    #PID control parameters
    kp_x=1.3# Proportional coefficient, X direction
    ki_x=1.25# Integral coefficient, X direction
    kd_x=1.75# Differential coefficient, X direction

    kp_y=30 # Proportional coefficient, Y direction
    ki_y=40 # Integral coefficient, Y direction
    kd_y=15 # Differential coefficient, Y direction


    kp_attitude=5 # Proportional coefficient, attitude
    ki_attitude=0.5 # Integral coefficient, attitude
    kd_attitude=1.25 # Differential coefficient, attitude

    error_x=state[0]-target_pos[0] # Calculate the error in the x-direction
    error_y=state[1]-target_pos[1] # Calculate the error in the y-direction
    
    integral_x += error_x * dt # Update the integral in the x-direction
    integral_y += error_y * dt # Update the integral in the y-direction
    integral_x = max(min(integral_x, 0.01), -0.01) # Limit the integral in the x-direction
    integral_y = max(min(integral_y, 0.2), -0.2) # Limit the integral in the y-direction
    
    # Outer loop controller
    phic=-1/g*(kp_x*error_x+ki_x*integral_x + kd_x*(state[2])) # Calculate attitude control targets in the x-direction
    phic = max(min(phic, 0.1745), -0.1745) #Limiting the angle of flight of the UAV

    # Inner loop controller:
    error_attitude=state[4]-phic # Calculate the attitude error in the x direction


    integral_attitude += error_attitude * dt # Update the integral term of the attitude 
    integral_attitude=max(min(integral_attitude,0.01),-0.01) # Limit the integral in the x-direction

    F=m*(g+kp_y*error_y+ki_y*integral_y+kd_y*state[3]) # Calculate motor thrust
    M=uav_inertia*(kp_attitude*error_attitude + ki_attitude*integral_attitude+kd_attitude*(state[5])) # Calculate motor torque


    u1=0.5*(F-M/arm_length) #Calculate the throttle setting for the left motor
    u2=0.5*(F+M/arm_length) #Calculate the throttle setting for the right motor

    u_1 = min(max(0, u1), 1) # Limit the throttle setting of the left motor
    u_2= min(max(0, u2), 1)  # Limit the throttle setting of the right motor

    return (u_1, u_2) # Returns the throttle settings of the left and right motors

    # state format: [position_x (m), position_y (m), velocity_x (m/s), velocity_y (m/s), attitude(radians), angular_velocity (rad/s)]
    # target_pos format: [x (m), y (m)]
    # dt: time step
    # return: action format: (u_1, u_2)
    # u_1 and u_2 are the throttle settings of the left and right motor

    
    


