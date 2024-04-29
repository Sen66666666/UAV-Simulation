from src.environment import Environment
import controller
import pygame_gui
import pygame
import csv
import sys
import importlib
import pathlib


import csv



targets = []
with open("targets.csv", "r") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        if (
            float(row[0]) > 8
            or float(row[1]) > 8
            or float(row[0]) < 0
            or float(row[1]) < 0
        ):
            print(
                "WARNING: Target outside of environment bounds (0, 0) to (8, 8), not loading target"
            )
        else:
            targets.append((float(row[0]), float(row[1])))

environment = Environment(
    render_mode="human",
    render_path=True,
    screen_width=1000,
    ui_width=200,
    rand_dynamics_seed=controller.group_number,
    wind_active=controller.wind_active,
)



running = True
target_pos = targets[0]


theme_path = pathlib.Path("src/theme.json")
manager = pygame_gui.UIManager(
    (environment.screen_width, environment.screen_height), theme_path
)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((800, 0), (200, 50)),
    text="Reset",
    manager=manager,
)

wind_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((800, 50), (200, 50)),
    text="Toggle Wind",
    manager=manager,
)

target_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((800, 700), (200, 50)),
    text="Target: " + str(target_pos),
    manager=manager,
)

prev_target_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((800, 750), (100, 50)),
    text="Prev",
    manager=manager,
)

next_target_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((900, 750), (100, 50)),
    text="Next",
    manager=manager,
)


def reload():
    # re importing the controller module without closing the program
    try:
        importlib.reload(controller)
        environment.reset(controller.group_number, controller.wind_active)

    except Exception as e:
        print("Error reloading controller.py")
        print(e)

def save_data_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        if filename == 'velocity_data.csv':
            writer.writerow(['Timestamp (s)', 'Velocity X', 'Velocity Y'])
        elif filename == 'attitude_data.csv':
            writer.writerow(['Timestamp (s)', 'Attitude '])
        elif filename == 'angular_velocity_data.csv':
            writer.writerow(['Timestamp (s)', 'Angular Velocity '])
        writer.writerows(data)


def check_action(unchecked_action):
    # Check if the action is a tuple or list and of length 2
    if isinstance(unchecked_action, (tuple, list)):
        if len(unchecked_action) != 2:
            print(
                "WARNING: Controller returned an action of length "
                + str(len(unchecked_action))
                + ", expected 2"
            )
            checked_action = (0, 0)
            pygame.quit()
            sys.exit()
        else:
            checked_action = unchecked_action

    else:
        print(
            "WARNING: Controller returned an action of type "
            + str(type(unchecked_action))
            + ", expected list or tuple"
        )
        checked_action = (0, 0)
        pygame.quit()
        sys.exit()

    return checked_action



# Game loop
velocity_data = []  # 初始化数据存储列表
attitude_data = []
angular_velocity_data = []
while running:
    #print("the current mass：", environment.drone.mass, "kg")
    #print("the current rotational_inertia：",environment.drone.rotational_inertia,"kg*m**2")
    print("the velocity：",environment.drone.velocity,"m/s")

    state = environment.drone.get_state()
    velocity_data.append([pygame.time.get_ticks() / 1000.0, state[2], state[3]])
    attitude_data.append([pygame.time.get_ticks() / 1000.0, state[4]]) 
    angular_velocity_data.append([pygame.time.get_ticks() / 1000.0, state[5]])   # 收集数据

    time_delta = environment.clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data_to_csv(velocity_data, 'velocity_data.csv')
            save_data_to_csv(attitude_data, 'attitude_data.csv')
            save_data_to_csv(angular_velocity_data, 'angular_velocity_data.csv')# 在退出前保存数据到CSV
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == reset_button:
                reload()
            if event.ui_element == wind_button:
                environment.toggle_wind()
            if event.ui_element == prev_target_button:
                target_pos = targets[targets.index(target_pos) - 1]
                target_label.set_text("Target: " + str(target_pos))
            if event.ui_element == next_target_button:
                target_pos = targets[(targets.index(target_pos) + 1) % len(targets)]
                target_label.set_text("Target: " + str(target_pos))
                

        manager.process_events(event)

    # Get the state of the drone
    state = environment.drone.get_state()
    # Call the controller function
    action = check_action(controller.controller(state, target_pos, 1 / 60))

    environment.step(action)

    manager.update(time_delta)
    environment.render(manager, target_pos)

    




