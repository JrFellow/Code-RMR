import time
import pygame
import random
import auth
import re
import asyncio


# define the window
class Content:
    def __init__(self, title, x, y, fps, user):
        self.title = title
        self.x = x
        self.y = y
        self.fps = fps
        self.user = user
class Authentication(Content): # everything auth-based
    def __init__(self, first_name, last_name, pin, password, coins): # Initialize first name, last name, password and coins for authentication
        self.first_name = first_name
        self.last_name = last_name
        self.pin = pin
        self.password = password
        self.coins = coins
        Content.user = [self.first_name, self.last_name, self.pin, self.password, self.coins]

    def number_letter_conversion(numbers):
        #Define a dictionary mapping numbers to letters
        mapping = {
            0: "A", 1: "C", 2: "B", 3: "D", 4: "F", 
            5: "E", 6: "G", 7: "H", 8: "I", 9: "J"
        }
        result = ""
        for digit in str(numbers):
            if int(digit) in mapping:
                result += mapping[int(digit)]
        return result
    def read_auth_file(filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content


    def write_auth_file(content, filename):
        with open(filename, 'w') as file:
            file.write(content)

    def update_user_credential(username, credential_index, new_value, filename):
        content = Authentication.read_auth_file(filename)
        pattern = re.compile(rf'{username}\s*=\s*\[.*\]')
        match = re.search(pattern, content)
        if match:
            start_index = match.start()
            end_index = match.end()
            updated_line = content[start_index:end_index]
            updated_line_parts = updated_line.split(',')
            #print(updated_line, updated_line_parts)
            
            
            #updated_line_parts_list = updated_line_parts.replace("")
            # Convert new value to an integer
            try:
                new_value_int = int(new_value)
            except ValueError:
                print("Error: New value must be an integer.")
                return
            updated_line_parts_before_change = updated_line_parts[credential_index].replace("]", "")
            updated_line_parts[credential_index] = f" {int(updated_line_parts_before_change) + new_value_int}" + "]"
            updated_line = ','.join(updated_line_parts)
            content = content[:start_index] + updated_line + content[end_index:]
            Authentication.write_auth_file(content, filename)
            print(f"User '{username}' credential updated successfully.")
        else:
            print(f"User '{username}' not found.")

class pygame_helper:
    def render_multiline_text(text, custom_font, text_color, x, y, line_spacing):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            text_surface = custom_font.render(line, True, text_color)
            screen.blit(text_surface, (x, y + i * (custom_font.get_height() + line_spacing)))
    def render_multiline_text_color(text_lines, custom_font, x, y, colors):
        for i, (line, color) in enumerate(zip(text_lines, colors)):
            text_surface = custom_font.render(line, True, color)
            screen.blit(text_surface, (x, y + i * custom_font.get_height()))


app = Content(title="Rapid Math Racing", x=700, y=725, fps=60,user=None)
user = None # defined in the auth screens
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((app.x, app.y), pygame.RESIZABLE)
pygame.display.set_caption(app.title)

coins = 0
# set font
font = pygame.font.SysFont("Roboto", 48)
paragraph_font = pygame.font.SysFont("Roboto", 25)
medium_font = pygame.font.SysFont("Roboto", 40)
medium2_font = pygame.font.SysFont("Roboto", 35)

# fps
clock = pygame.time.Clock()
async def main():
    def game_result_screen(result):
        Reward = False # indicate if reward is deserved

        result_text = "Error 404" # Just for debugs or default value

        home_button_image = pygame.image.load("assets/home_button.png")
        resized_home_button_image = pygame.transform.smoothscale(home_button_image, (50, 50))
        home_button_image_rect = resized_home_button_image.get_rect()

        if result == "user":
            result_text = "YOU WON!!"
            Reward = True
            reward_coins = random.randint(999, 5200)
            coin_image = pygame.image.load("assets/coin_image.png")
            resized_coin_image = pygame.transform.smoothscale(coin_image, (50, 50))
        if result == "computer":
            result_text = "You lost."
        if result == "tie":
            result_text = "You tied the game."
        reward_given_once = False
        run = True
        while run:  # loop while the code is running
            for event in pygame.event.get():  # event handler
                if event.type == pygame.QUIT:
                    run = False  # stop running code
                    pygame.quit()  # clear stop running code
                    #exit()  # confirm stop running code
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if home_button_image_rect.collidepoint(pygame.mouse.get_pos()):
                            return home_screen()
            screen.fill((255, 255, 255)) # Just for now 
            show_result_text = font.render(result_text, True, (0, 0, 0)) # Render the text of the result
            screen.blit(show_result_text, (app.x // 2 - 100, app.y // 2 - 300))
            if Reward == True:
                if reward_given_once == False:
                    Content.user[4] = Content.user[4] + reward_coins
                    pin_text_conversion = Authentication.number_letter_conversion(Content.user[2])
                    Authentication.update_user_credential(pin_text_conversion, 4, reward_coins, "auth.py")
                    reward_given_once = True
                reward_text = font.render(str(reward_coins), True, (250, 204, 77))
                screen.blit(reward_text, (app.x // 2 - 135, app.y // 2 + 12.5))
                screen.blit(resized_coin_image, (app.x // 2 - 200, app.y // 2))
                screen.blit(resized_home_button_image, (0, 0))
            pygame.display.flip()
            # control fps
            clock.tick(app.fps)
    # for debug 
    #game_result_screen("user")
            


    def game_screen():
        global screen
        # set up background
        background = pygame.image.load("assets/background.png")
        original_background = pygame.transform.smoothscale(background, (700, 725))

        finish_background = pygame.image.load("assets/finish_background.png")
        finish_background2 = pygame.transform.smoothscale(finish_background, (700, 725))

        user_car_image = pygame.image.load("assets/user_car.png")
        user_car_image2 = pygame.transform.smoothscale(user_car_image, (200, 200))
        user_car_rect = user_car_image2.get_rect()

        computer_car_image = pygame.image.load("assets/computer_car.png")
        computer_car_image2 = pygame.transform.smoothscale(computer_car_image, (200, 200))
        computer_car_rect = computer_car_image2.get_rect()

        # set up the car
        class car:
            def __init__(self, x, y, rect):
                self.x = x
                self.y = y
                rect.topleft = (self.x, self.y)

            def move(self, speed, endpoint):
                # accelerate the car by subtracting the y position
                moved = False
                self.speed = speed
                if self.y > endpoint and moved == False:
                    self.y -= speed
                elif self.y == endpoint:
                    moved = True
                    self.y = endpoint
            def reverse(self, speed, endpoint):
                reversed = False
                self.speed = speed
                if self.y < endpoint and reversed == False:
                    self.y += speed
                elif self.y == endpoint:
                    reversed = True
                    self.y = endpoint

        user_car = car(300, 325, user_car_rect)
        computer_car = car(200, 325, computer_car_rect)
        position = 0
        position1 = 0
        mph = 0

        def calculate_computer_speed(user_speed):
            while True:
                computer_speed = random.randint(2, 300)
                if abs(computer_speed - user_speed) <= 25:
                    return computer_speed
        def check_speed_is_less(computer_speed, user_speed):
            if computer_speed > user_speed:
                computer_car.move(computer_speed - user_speed, -40)

        def calculate_speed(time):
            if time >= 20:
                return 0
            elif time >= 15 < 20:
                return 25
            elif time >= 10 < 15:
                return 50
            elif time >= 8 < 10:
                return 100
            elif time >= 6 < 8:
                return 200
            elif time >= 4 < 6:
                return 250
            elif time >= 0 < 4:
                return 300



        #def calculate_position(background_pos, car_type, bgs, total_miles):
            #if car_type == "computer":
                #if background_pos == 0 and computer_car_rect.y
                    # Remember so i will reset the cvomputer car's y pos to the start and when its zero then new background, with a var that says reseted times.

        # rect info
        box_rect_color = ("#DBDBDB")

        # Set up the rectangle properties
        box_rect_width, box_rect_height = app.x, 200
        box_rect_x, box_rect_y = 0, app.y - box_rect_height

        def generate_math_question():
            # math problem set up
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            operators = ["x", "+", "-", "\u00F7"]
            operator = random.choice(operators)

            # Ensure division and subtraction meet criteria
            while (operator == "\u00F7" and (num1 % num2 != 0 or num1 - num2 < 0)) or (operator == "-" and num1 - num2 < 0):
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
            if operator == "x":
                answer = num1 * num2
            if operator == "+":
                answer = num1 + num2
            if operator == "-":
                answer = num1 - num2
            if operator == "\u00F7":
                answer = num1 / num2
            return num1, num2, answer, operator

        math_question = generate_math_question()
        user_answer = ""

        question_text = font.render(
            "What is " + str(math_question[0]) + " " + math_question[3] + " " + str(math_question[1]) + "?", True,
            ("#4C4E52"))
        question_rect = pygame.Rect(225, 600, 250, 45)
        question_rect_color = (0, 0, 0)
        active = True  # the question box if the box is in the phase of typing
        COMPUTER_Y = 325  # constant for Computer car's position
        USER_Y = 325  # constant for User car's position
        user_miles = 0  # to check if user car is in a place where computer car should not be visible
        computer_miles = 0  # to help check if user car is in a place where computer car should not be visible
        computer_car_visible = True  # to indicate if the computer car should be visible or not depending on user_miles and computer_miles
        user_car_visible = True
        animation = False
        boost_text = ""
        textB = ""
        Bnum = 0

        stop = False  # to control stopwatch
        show_result = False  # result show
        asked_times = 1  # AI part
        total_miles = 1000  # total miles (also total backgrounds to pass)
        total_miles = 1000  # total miles (also total backgrounds to pass)
        color = None
        questions_correct = 0
        questions_incorrect = 0
        computer_car_pos_reset = 0
        user_car_pos_reset = 0

        bgs = 0 # backgrounds that had been gone through | 1 background = 1 mile
        bgs1 = 0
        n = True
        y = False  # To control the background's image
        m = False  # to calculate computer speed once in "if show_result == None" when answer is correct
        j = False  # to calculate computer speed once in "if show_result == True" when answer is incorrect
        f = False  # to control animation background's image
        s = False  # to reduce user's speed when incorrect once
        x = False
        timer = 0  # the stopwatch for how much time the user took to answer the math question
        timer2 = 0  # the stopwatch until a new question appears
        stop_moving = False  # the Computer car's endpoint in code (meaning not in object function)
        stop_moving2 = False  # the User car's endpoint in code (meaning not in object function)
        run = True  # to identify if the code is running

        while run:  # loop while the code is running
            for event in pygame.event.get():  # event handler
                if event.type == pygame.QUIT:
                    run = False  # stop running code
                    pygame.quit() # clear stop running code
                    #exit()  # confirm stop running code
                elif event.type == pygame.VIDEORESIZE:
                    # update
                    app.x, app.y = event.size
                    screen = pygame.display.set_mode((app.x, app.y), pygame.RESIZABLE)
                    original_background = pygame.transform.smoothscale(background, (app.x, app.y))

                    box_rect_y = app.y - box_rect_height
                    box_rect_width = app.x
                    question_rect_x = app.x // 2 - question_rect.width // 2
                    question_rect_y = app.y - 135
                    question_rect.topleft = (question_rect_x, question_rect_y)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if active == False:
                        if question_rect.collidepoint(event.pos):
                            active = True
                            question_rect_color = (0, 0, 255)
                    else:
                        active = False
                        question_rect_color = (0, 0, 0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_answer != "":
                        stop = True
                        if int(user_answer) == int(math_question[2]):
                            mph = 20
                            show_result = None
                        if int(user_answer) != int(math_question[2]):
                            show_result = True
                    if active == True:
                        if event.key == pygame.K_BACKSPACE:
                            user_answer = user_answer[:-1]
                        else:
                            if event.unicode.isnumeric():
                                user_answer += event.unicode
            # screen.fill(0, 0, 0)
            if animation == False:
                if bgs == total_miles:  # the phase of showing the finish line background
                    y = True
                    screen.blit(finish_background2, (0, 0))
                    screen.blit(finish_background2, (0, 0))
                elif bgs < total_miles:
                    screen.blit(original_background, (0, position))
                    screen.blit(original_background, (0, original_background.get_height() + position))
                position -= mph
                miles_away_finish = total_miles - bgs
                if y != True:
                    if abs(position) > original_background.get_height():

                        position = 0
                        bgs = bgs + 1

                if y == True:
                    user_car.move(mph / 30, 0)
                    computer_car.move(round((mph / 30) - random.randint(0, 5), 2), 0)
                    if computer_car_visible == True and user_car_visible == True:
                        if user_car_rect.y <= 0 and computer_car_rect.y <= 0:
                            game_result_screen("tie")
                    else:
                        if user_car_rect.y <= 0 and computer_car_visible == False:
                            time.sleep(0.75)
                            game_result_screen("user")
                        if computer_car_rect.y <= 0 and user_car_visible == False:
                            game_result_screen("computer")
                #raise Exception("gf")
            try:

                if mph > computer_speed_result and computer_miles > user_miles:
                    computer_car.reverse(mph - computer_speed_result, user_car_rect.y - 20)
            except:
                pass
            if computer_car_visible == True and user_car_rect.y > computer_car_rect.y and computer_speed_result > mph:
                #user_car.reverse(abs(mph // 60), computer_speed_result + mph)
                computer_car.move(5, computer_speed_result + mph)
            # 1 boost by computer = 100 mi
            try:
                if computer_speed_result > mph:
                    if computer_speed_result >= 1 < 50:
                        if computer_miles - user_miles > 16:
                            animation = True
                    if computer_speed_result >= 50 <= 100:
                        if computer_miles - user_miles > 12:
                            animation = True
                    if computer_speed_result > 100 <= 200:
                        if computer_miles - user_miles > 10:
                            animation = True
                    if computer_speed_result > 200 < 300:
                        if computer_miles - user_miles > 9:
                            animation = True

            except:
                pass
            if mph < 0:
                mph = 0

            if user_car_rect.y <= -40:
                user_car.y = 420
                user_car_rect.y = 420
                user_miles = user_miles + 1
            if computer_car_rect.y <= -40:
                computer_car.y = 420
                computer_car_rect.y = 420
                computer_miles = computer_miles + 1

            if abs(computer_miles - user_miles) > 0:
                computer_car_visible = False
            else:
                computer_car_visible = True
            # debugs and drawings:

            # if computer_car_speed > result:
            # user_car.move(1, 130)

            user_car_rect.topleft = (user_car.x, user_car.y)
            computer_car_rect.topleft = (computer_car.x, computer_car.y)
            # if user_car_rect.y
            screen.blit(user_car_image2, user_car_rect)
            if computer_car_visible == True:
                screen.blit(computer_car_image2, computer_car_rect)
            # draw the rectangles
            pygame.draw.rect(screen, box_rect_color, (box_rect_x, box_rect_y, box_rect_width, box_rect_height))
            pygame.draw.rect(screen, question_rect_color, question_rect, 2)
            user_answer_surface = font.render(user_answer, True, (0, 0, 0))
            screen.blit(user_answer_surface, (question_rect.x + 5, question_rect.y + 5))
            question_x = app.x // 2 - question_text.get_width() // 2
            question_y = app.y - 175
            speed_text = font.render("Speed: " + str(mph), True, ("#4C4E52"))
            screen.blit(speed_text, (app.x - 180, 0))

            try:
                computer_speed_text = font.render("Computer Speed: " + str(computer_speed_result), True, ("#4C4E52"))
            except:
                computer_speed_text = font.render("Computer Speed: 0", True, ("#4C4E52"))
            screen.blit(computer_speed_text, (0, 0))

            miles_away_finish_text = paragraph_font.render("Miles left: " + str(miles_away_finish) + " miles" if total_miles - bgs > 1 else "Miles left: Nearby!", True, ("#4C4E52"))
            screen.blit(miles_away_finish_text, (app.x - 180, app.y - 225))

            user_text = paragraph_font.render("You", True, ("#4C4E52"))
            screen.blit(user_text, (user_car_rect.x + 85, user_car_rect.y - 20))

            computer_text = paragraph_font.render("Computer", True, ("#4C4E52"))
            if computer_car_visible == True:
                screen.blit(computer_text, (computer_car_rect.x + 57, computer_car_rect.y - 20))
            if stop == False:
                timer += 1
                secs = timer // 60
                if secs >= 20 and mph > 0:
                    check_speed_is_less(computer_speed_result, mph)
                    secs = 20
                    mph -= 1

                text = font.render(f"Elapsed: {secs} seconds", True, (0, 0, 0))
                screen.blit(text, (25, app.y - 40))


            # screen.blit(question_text, (question_x, question_y))
            # screen.blit(original_user_car_image, (200, 200))
            screen.blit(question_text, (240, 550))
            if show_result == True:
                if s == False:
                    mph -= 25
                    s = True
                questions_incorrect += 1

                timer2 += 1
                secs2 = timer2 // 60
                if j == False:
                    computer_speed_result = calculate_computer_speed(user_speed=mph)
                    j = True
                if COMPUTER_Y or computer_car_rect.y == 0:
                    COMPUTER_Y -= 1
                    computer_car_rect.y -= 1
                endpoint = COMPUTER_Y - abs(user_car_rect.y)
                if stop_moving2 == False:
                    computer_car.move(abs(secs2 + computer_speed_result // 60) if mph > 0 else computer_speed_result, endpoint if mph > 0 else -50)
                    if x == False:
                        computer_speed_result += 5
                        x = True



                if computer_car_rect.y <= endpoint if mph > 0 else computer_car_rect.y <= -50:
                    stop_moving2 = True
                    COMPUTER_Y = endpoint
                    #computer_car.move(5, 0)



                reply_text = font.render("Incorrect.", True, ("#4C4E52"))
                screen.blit(reply_text, (25, 10))
                time_results_text = paragraph_font.render(
                    "You took " + str(secs) + " seconds to complete your math question", True, ("#4C4E52"))
                screen.blit(time_results_text, (question_rect.x - 100, app.y - question_rect.w + 200))

                question_rect_color = (0, 0, 0)
                active = None
                if secs2 == 5:
                    x = False
                    s = False
                    stop_moving = False
                    stop_moving2 = False
                    show_result = False
                    m = False
                    j = False
                    user_answer = ""
                    timer2 = 0
                    math_question = generate_math_question()
                    asked_times += 1

                    question_text = font.render(
                        "What is " + str(math_question[0]) + " " + math_question[3] + " " + str(math_question[1]) + "?",
                        True, ("#4C4E52"))
                    stop = False
                    timer = 0
                    secs = 0
                    secs2 = 0

            if show_result == None:
                questions_correct += 1
                reply_text = font.render("Correct!", True, ("#4C4E52"))
                screen.blit(reply_text, (25, 10))

                time_results_text = paragraph_font.render(
                    "You took " + str(secs) + " seconds to complete your math question", True, ("#4C4E52"))
                screen.blit(time_results_text, (question_rect.x - 100, app.y - question_rect.w + 200))

                timer2 += 1
                secs2 = timer2 // 60
                active = None
                question_rect_color = (0, 0, 0)

                user_speed_result = calculate_speed(secs)
                mph = user_speed_result
                if m == False:
                    computer_speed_result = calculate_computer_speed(user_speed=mph)
                    m = True

                if computer_speed_result is not None:
                    if computer_speed_result > mph:
                        ENDPOINT_COMPUTER = COMPUTER_Y - computer_speed_result + 20
                        if stop_moving == False:
                            computer_car.move(abs(computer_speed_result), ENDPOINT_COMPUTER)
                        if computer_car_rect.y <= ENDPOINT_COMPUTER:
                            stop_moving = True
                            COMPUTER_Y = ENDPOINT_COMPUTER
                    elif mph > computer_speed_result:
                        ENDPOINT_USER = USER_Y - mph + 20
                        if stop_moving2 == False:
                            user_car.move(abs(secs2 + mph // 60), ENDPOINT_USER)
                            boost_text = True
                            textB = str(abs(secs2 + computer_speed_result // 60) / 40 * 100) + "% Boost!"
                            Bnum = abs(secs2 + computer_speed_result // 60)
                        if user_car_rect.y <= ENDPOINT_USER:
                            stop_moving2 = True
                            USER_Y = ENDPOINT_USER


                if secs2 == 5:
                    stop_moving = False
                    stop_moving2 = False
                    mph = mph - Bnum
                    question_rect_color = (0, 0, 255)
                    active = True
                    show_result = False
                    m = False
                    user_answer = ""
                    timer2 = 0
                    math_question = generate_math_question()
                    asked_times += 1

                    question_text = font.render(
                        "What is " + str(math_question[0]) + " " + math_question[3] + " " + str(math_question[1]) + "?",
                        True, ("#4C4E52"))
                    stop = False
                    timer = 0
                    secs = 0
                    secs2 = 0
                if boost_text == True and stop_moving == False:
                    if secs2 == 0:
                        color = (0, 0, 255)
                    if secs2 == 1:
                        color = (127, 0, 255)
                    if secs2 == 2:
                        color = (255, 0, 0)
                    if secs2 == 3:
                        color = (170, 255, 0)
                    if secs2 == 4:
                        color = (80, 200, 120)
                    if secs2 < 5:
                        mph = mph + Bnum

                    textB2 = medium_font.render(textB, True, color)
                    screen.blit(textB2, (app.x - 180, 35))
            if animation == True:
                if bgs1 == 100:  # the phase of showing the finish line background
                    f = True
                    screen.blit(finish_background2, (0, 0))
                    screen.blit(finish_background2, (0, 0))
                elif bgs1 < 100:
                    screen.blit(original_background, (0, position1))
                    screen.blit(original_background, (0, original_background.get_height() + position1))
                if bgs1 > 50:
                    user_car_visible = False
                if user_car_visible == True:
                    user_car.reverse(5, 800)
                    screen.blit(user_car_image2, user_car_rect)
                position1 -= 200
                if f != True:
                    if abs(position1) > original_background.get_height():
                        position1 = 0
                        bgs1 = bgs1 + 1

            

                if f == True:
                    screen.blit(computer_car_image2, computer_car_rect)
                    if n == False:
                        computer_car_rect.y = 420
                        n = True
                    computer_car.move(10, -0)
                    if computer_car_rect.y == -0:
                        game_result_screen("computer")
            pygame.display.flip()
            # control fps
            clock.tick(app.fps)


    # for test
    #game_screen()

    def game_countdown_screen():
        run = True    
        timer = 4 * 1000  # 4 seconds in milliseconds
        stop = False
        run = True    
        timer = 4 * 1000  # 4 seconds in milliseconds
        stop = False
        
        while run:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    run = False  
                    pygame.quit()    
            
            screen.fill((0, 0, 0))
            timer -= clock.get_time()
            # Calculate remaining seconds
            secs = max(0, timer // 1000)  # Convert milliseconds to seconds
            if not stop:
                timer_text = font.render("Starting in " + str(secs), True, (255, 255, 255))
            if secs == 0:  # Display "Go!" when countdown reaches 1
                stop = True
            if stop:
                timer_text = font.render("Go!", True, (255, 255, 255))
                screen.blit(timer_text, (50, 50))
                pygame.display.flip()
                pygame.time.delay(1000)  # Wait for 1 second before transitioning to game_screen
                game_screen()
            
            screen.blit(timer_text, (50, 50))
            pygame.display.flip()
            # control fps
            clock.tick(app.fps)

    def home_screen():
        coin_image = pygame.image.load("assets/coin_image.png")
        resized_coin_image = pygame.transform.smoothscale(coin_image, (50, 50))

        settings_icon = pygame.image.load("assets/settings_icon.png")
        settings_icon2 = pygame.transform.smoothscale(settings_icon, (55, 55))
        settings_icon_rect = settings_icon2.get_rect(topleft=(0, 15))

        tesla_roadster_image = pygame.image.load("assets/default_car.png")
        tesla_roadster = pygame.transform.smoothscale(tesla_roadster_image, (400, 200))

        background = ("#f5f5f5")

        top_bar_rect_dimensions = pygame.Rect(0, 0, app.x, 80)

        log_out_button_rect = pygame.Rect(app.x // 7, 25, 150, 50)

        race_buttton_rect = pygame.Rect(app.x / 1.5, app.y - 100, 150, 50)

        settings_app = pygame.Surface((350, 300))
        def settings_screen():
            settings_app.fill((255, 255, 255))
            pygame.draw.rect(settings_app, pygame.Color("red"), log_out_button_rect, border_radius=10)
            log_out_text_surface = medium_font.render("Log Out", True, (255, 255, 255))
            log_out_text_rect = log_out_text_surface.get_rect(center=log_out_button_rect.center)
            settings_app.blit(log_out_text_surface, log_out_text_rect)
            screen.blit(settings_app, (app.x // 4, app.y // 3.5))
            
        change_x = False
        show_settings = False
        run = True
        while run:  # loop while the code is running
            for event in pygame.event.get():  # event handler
                if event.type == pygame.QUIT:
                    run = False  # stop running code
                    pygame.quit()  # clear stop running code
                    #exit()  # confirm stop running code
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_pos_in_settings_app = mouse_pos[0] - app.x // 4, mouse_pos[1] - app.y // 3.5
                    if event.button == 1:
                        if settings_icon_rect.collidepoint(pygame.mouse.get_pos()):
                
                            show_settings = True
                        if race_buttton_rect.collidepoint(pygame.mouse.get_pos()):
                            game_countdown_screen()           
                        if log_out_button_rect.collidepoint(mouse_pos_in_settings_app):
                            return welcome_screen()
                            Content.user = None
                        if not settings_app.get_rect().collidepoint(event.pos):
                            show_settings = False
                        
            screen.fill(background)
            pygame.draw.rect(screen, ("#595959"), top_bar_rect_dimensions)# top bar
            pygame.draw.rect(screen, ("#FFAB40"), race_buttton_rect, border_radius=10)
            race_button_text_surface = font.render("Race", True, (255, 255, 255))
            race_button_text_rect = race_button_text_surface.get_rect(center=race_buttton_rect.center)
            screen.blit(race_button_text_surface, race_button_text_rect)

            welcome_text = medium2_font.render("Hello there, Racer " + Content.user[0] + "!", True, ("#f5f5f5"))
            screen.blit(welcome_text, (app.x // 3, 25))

            Race_text = medium_font.render("Race for more coins!", True, ("#FFAB40"))
            screen.blit(Race_text, (race_buttton_rect.x - 75, race_buttton_rect.y - 50))

            specs_text = medium2_font.render("Specs:", True, ("#4C4E52"))
            screen.blit(specs_text, (app.x // 2 + 150 // 2, app.y // 2 - 255))

            # specs text code(
            
            twentytozero = paragraph_font.render("20 sec- 0 mph", True, ("#762023"))
            screen.blit(twentytozero, (app.x // 2 + 150 // 2, app.y // 2 - 67 - 100)) 

            fifteentotwentyfive = paragraph_font.render("15 sec- 25 mph", True, (255, 0, 0))
            screen.blit(fifteentotwentyfive, (app.x // 2 + 150 // 2, app.y // 2 - 67 - 50))

            tentofifty = paragraph_font.render("10 sec- 50 mph", True, ("#B45F06"))
            screen.blit(tentofifty, (app.x // 2 + 150 // 2, app.y // 2 - 67))

            #pygame_helper.render_multiline_text("You need to\npractice your\nMath facts more!", paragraph_font, (255, 0, 0), app.y // 2 + 400 // 2 , app.y // 2 - 67 - 70, line_spacing=0)
            spec1_text = ["You need to", "practice your", "Math facts more!"]
            spec1_colors = [("#762023"), (255, 0, 0), ("#B45F06")]
            pygame_helper.render_multiline_text_color(text_lines=spec1_text, custom_font=paragraph_font, x=app.y // 2 + 400 // 2 , y=app.y // 2 - 67 - 70, colors=spec1_colors)

            eighttohundred = paragraph_font.render("8 sec- 100 mph", True, (255, 165, 0))
            screen.blit(eighttohundred, (app.x // 2 + 150 // 2, app.y // 2 - 67 - -50))

            sixtotwohundred = paragraph_font.render("6 sec- 200 mph", True, ("#F1C232"))
            screen.blit(sixtotwohundred, (app.x // 2 + 150 // 2, app.y // 2 - 67 - -100))

            spec2_text = ["Okay, you're", "getting there!"]
            spec2_colors = [(255, 165, 0), ("#F1C232")]
            pygame_helper.render_multiline_text_color(text_lines=spec2_text, custom_font=paragraph_font, x=app.y // 2 + 400 // 2, y=app.y // 2 - 67 - -70, colors=spec2_colors)

            fourtotwofifty = paragraph_font.render("4 sec- 250 mph", True, ("#90EE90"))
            screen.blit(fourtotwofifty, (app.x // 2 + 150 // 2, app.y // 2 - 67 - -150))

            twototreehundred = paragraph_font.render("2 sec- 300 mph", True, ("#38761D"))
            screen.blit(twototreehundred, (app.x // 2 + 150 // 2, app.y // 2 - 67 - -200))


            spec3_text = ["You are the", "ultimate Math", "Racer!"]
            spec3_colors = [("#90EE90"), ("#38761D"), ("#38761D")]
            pygame_helper.render_multiline_text_color(text_lines=spec3_text, custom_font=paragraph_font, x=app.y // 2 + 400 // 2, y=app.y // 2 - 67 - -170, colors=spec3_colors)




            # end of specs text code )

            your_car_text = medium_font.render("Your car", True, (0, 0, 0))
            screen.blit(your_car_text, (app.x // 2 - 230, app.y // 2 - 235))

            car_name_text = paragraph_font.render("Tesla Roadster (2011)", True, ("#4C4E52"))
            screen.blit(car_name_text, (app.x // 2 - 230 * 1.1, app.y // 2 - 235 // 2 - 50))

            screen.blit(settings_icon2, settings_icon_rect)

            reward_text = font.render(str(Content.user[4]), True, (250, 204, 77))
            # screen.blit(reward_text, (app.x // 2 - 135, app.y // 2 + 12.5))

            # screen.blit(resized_coin_image, (app.x // 2 - 200, app.y // 2))
            reward_text_width, reward_text_height = reward_text.get_size()

            screen.blit(tesla_roadster, (0, 250))
            screen.blit(reward_text, (app.x - reward_text_width - 10, 25))
            #screen.blit(reward_text, (app.x - 35, 25))
            screen.blit(resized_coin_image, (app.x - reward_text_width - 70, 15))
            if show_settings == True:
                darker_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                darker_surface.fill((0, 0, 0, 155))
                screen.blit(darker_surface, (0, 0))
                settings_screen()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and show_settings:
                    if event.button == 1 and not settings_app.get_rect(topleft=(app.x // 4, app.y // 3.5)).collidepoint(event.pos):
                        show_settings = False 
            #control fps
            clock.tick(app.fps)
    # for test
    # home_screen()

    def login_screen():
        password_visible = False
        background = ("#f5f5f5")
        # Show Password button
        show_password_rect = pygame.Rect(200, 277, 275, 50)
        show_password_color = ("#f5f5f5")
        show_password_text = font.render("Show Password", True, (0, 0, 0))
        show_password_text_rect = show_password_text.get_rect(center=show_password_rect.center)
        # back button
        original_back_button_image = pygame.image.load("assets/back.png")
        back_button_image = pygame.transform.smoothscale(original_back_button_image, (50, 50))
        back_button_rect = back_button_image.get_rect()
        # forward button
        original_forward_button_image = pygame.image.load("assets/forward.png")
        forward_button_image = pygame.transform.smoothscale(original_forward_button_image, (100, 100))
        forward_button_rect = forward_button_image.get_rect()
        # rect info
        password_rect_x, password_rect_y = 200, 200
        password_rect_width, password_rect_height = 275, 65

        pin_rect_x, pin_rect_y = 200, 400
        pin_rect_width, pin_rect_height = 137.5, 65

        pin_rect_outline_color = (0, 0, 0)
        password_rect_outline_color = (0, 0, 0)

        pin_input_active = False
        password_input_active = False

        pin_text = ""
        password_text = ""
        visible_password = ""
        run = True
        show = False
        show2 = False
        # main loop
        while run:
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit() # clear stop running code
                    #exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                            return access_screen()
                        if pin_rect_x < event.pos[0] < pin_rect_x + pin_rect_width and pin_rect_y < event.pos[
                            1] < pin_rect_y + pin_rect_height:
                            pin_input_active = True

                            pin_rect_outline_color = (0, 0, 255)
                        else:
                            pin_input_active = False
                            pin_rect_outline_color = (0, 0, 0)
                        if password_rect_x < event.pos[0] < password_rect_x + password_rect_width and password_rect_y < \
                                event.pos[1] < password_rect_y + password_rect_height:
                            password_input_active = True

                            password_rect_outline_color = (0, 0, 255)
                        else:
                            password_input_active = False
                            password_rect_outline_color = (0, 0, 0)
                        forward_button_rect = forward_button_image.get_rect(topleft=(600, 600))
                        if forward_button_rect.collidepoint(event.pos):
                            if pin_text and password_text != "":
                                auth_file_data = {}
                                with open("auth.py", "r") as auth_file:
                                    exec(auth_file.read(), auth_file_data)
                                pin_text_conversion = Authentication.number_letter_conversion(pin_text)
                                if pin_text_conversion in auth_file_data:
                                    user_credentials = auth_file_data[pin_text_conversion]
                                    if password_text == user_credentials[3]:
                                        app.user = Authentication(user_credentials[0], user_credentials[1], user_credentials[2], user_credentials[3], 0)
                                        home_screen()
                                    else:
                                        show = True
                                else:
                                    show = True
                            else:
                                show2 = True

                        if show_password_rect.collidepoint(event.pos):
                            password_visible = not password_visible
                elif event.type == pygame.KEYDOWN:
                    allowed_symbols = ["@", "$", "#", "!", "&", "*"]
                    if password_input_active:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                            visible_password = visible_password[:-1]
                        else:
                            if (event.unicode.isalnum() or event.unicode in allowed_symbols) and len(password_text) < 8:
                                password_text += event.unicode
                                # for privacy
                                visible_password += "*"



                    elif pin_input_active:
                        if event.key == pygame.K_BACKSPACE:
                            pin_text = pin_text[:-1]
                        else:
                            if event.unicode.isnumeric() and len(pin_text) < 4:
                                pin_text += event.unicode

            screen.fill(background)
            # draw rectangles
            pygame.draw.rect(screen, password_rect_outline_color,
                            (password_rect_x, password_rect_y, password_rect_width, password_rect_height), 2)
            pygame.draw.rect(screen, pin_rect_outline_color, (pin_rect_x, pin_rect_y, pin_rect_width, pin_rect_height), 2)

            # pin text in the rectangle
            pin_text_show = font.render(pin_text, True, (0, 0, 0))
            pin_text_rect = pin_text_show.get_rect(
                center=(pin_rect_x + pin_rect_width // 2, pin_rect_y + pin_rect_height // 2))
            screen.blit(pin_text_show, pin_text_rect)

            # Draw password text based on visibility
            password_text_show = font.render(password_text if password_visible else visible_password, True, (0, 0, 0))
            password_text_rect = password_text_show.get_rect(
                center=(password_rect_x + password_rect_width // 2, password_rect_y + password_rect_height // 2))
            screen.blit(password_text_show, password_text_rect)

            # Draw Show Password button
            pygame.draw.rect(screen, show_password_color, show_password_rect)
            screen.blit(show_password_text, show_password_text_rect)
            login = font.render("Welcome Back!", True, (0, 0, 0))
            screen.blit(login, (205, 13))
            password = font.render("Password", True, (0, 0, 0))
            screen.blit(password, (198, 160))
            pin = font.render("PIN", True, (0, 0, 0))
            screen.blit(pin, (198, 360))
            screen.blit(forward_button_image, (600, 600))
            screen.blit(back_button_image, (0, 0))
            if show == True:
                show_text = font.render("! Invaild PIN and password", True, (255, 0, 0))
                screen.blit(show_text, (25, 620))
            if show2 == True:
                show2_text = font.render("! Fill in all fields", True, (255, 0, 0))
                if password_text == "":
                    password_rect_outline_color = (255, 0, 0)
                if pin_text == "":
                    pin_rect_outline_color = (255, 0, 0)
                screen.blit(show2_text, (25, 520))

            pygame.display.flip()
            # control fps
            clock.tick(app.fps)


    def sign_up_screen():
        background = ("#f5f5f5")
        password_visible = False
        # Show Password button
        show_password_rect = pygame.Rect(298, 677, 275, 50)
        show_password_color = ("#f5f5f5")
        show_password_text = font.render("Show Password", True, (0, 0, 0))
        show_password_text_rect = show_password_text.get_rect(center=show_password_rect.center)
        # back button
        original_back_button_image = pygame.image.load("assets/back.png")
        back_button_image = pygame.transform.smoothscale(original_back_button_image, (50, 50))
        back_button_rect = back_button_image.get_rect()

        # forward button
        original_forward_button_image = pygame.image.load("assets/forward.png")
        forward_button_image = pygame.transform.smoothscale(original_forward_button_image, (100, 100))
        forward_button_rect = forward_button_image.get_rect()
        


        # check if any info in auth file
        info_in_authfile = False
        with open("auth.py", "r") as auth_file:
            if auth_file.read().strip():
                info_in_authfile = True

        first_name_text = ""
        last_name_text = ""
        pin_text = ""
        password_text = ""
        visible_password = ""

        # rect info
        first_name_rect_x, first_name_rect_y = 200, 200
        first_name_rect_width, first_name_rect_height = 275, 65

        last_name_rect_x, last_name_rect_y = 200, 400
        last_name_rect_width, last_name_rect_height = 275, 65

        password_rect_x, password_rect_y = 300, 600
        password_rect_width, password_rect_height = 275, 65

        pin_rect_x, pin_rect_y = 100, 600
        pin_rect_width, pin_rect_height = 137.5, 65

        first_name_rect_outline_color = (0, 0, 0)
        last_name_rect_outline_color = (0, 0, 0)
        pin_rect_outline_color = (0, 0, 0)
        password_rect_outline_color = (0, 0, 0)
        # you can type only when you click the rect
        first_name_input_active = False
        last_name_input_active = False
        pin_input_active = False
        password_input_active = False
        # if the form is not fully filled
        not_filled_fields = False
        # main loop
        run = True
        # checkmark
        checked = False
        # main loop
        while run:
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # exit code
                    run = False
                    pygame.quit()  # clear stop running code
                    #exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        first_name_rect_outline_color = (0, 0, 0)
                        last_name_rect_outline_color = (0, 0, 0)
                        pin_rect_outline_color = (0, 0, 0)
                        # Check if the mouse click is within the button area
                        if first_name_rect_x < event.pos[
                            0] < first_name_rect_x + first_name_rect_width and first_name_rect_y < event.pos[
                            1] < first_name_rect_y + first_name_rect_height:
                            first_name_input_active = True
                            last_name_input_active = False
                            first_name_rect_outline_color = (0, 0, 255)
                        else:
                            first_name_input_active = False
                            first_name_rect_outline_color = (0, 0, 0)
                        if last_name_rect_x < event.pos[0] < last_name_rect_x + last_name_rect_width and last_name_rect_y < \
                                event.pos[1] < last_name_rect_y + last_name_rect_height:
                            last_name_input_active = True
                            first_name_input_active = False
                            last_name_rect_outline_color = (0, 0, 255)
                        else:
                            last_name_input_active = False
                            last_name_rect_outline_color = (0, 0, 0)
                        if pin_rect_x < event.pos[0] < pin_rect_x + pin_rect_width and pin_rect_y < event.pos[
                            1] < pin_rect_y + pin_rect_height:
                            pin_input_active = True
                            first_name_input_active = False
                            last_name_input_active = False
                            pin_rect_outline_color = (0, 0, 255)
                        else:
                            pin_input_active = False
                            pin_rect_outline_color = (0, 0, 0)
                        if password_rect_x < event.pos[0] < password_rect_x + password_rect_width and password_rect_y < \
                                event.pos[1] < password_rect_y + password_rect_height:
                            password_input_active = True
                            first_name_input_active = False
                            last_name_input_active = False
                            password_rect_outline_color = (0, 0, 255)
                        else:
                            password_input_active = False
                            password_rect_outline_color = (0, 0, 0)

                        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                            return access_screen(), first_name_input_active, last_name_input_active, pin_input_active
                        forward_button_rect = forward_button_image.get_rect(topleft=(600, 600))
                        if forward_button_rect.collidepoint(event.pos):
                            if len(pin_text) == 4 and first_name_text != "" and last_name_text != "" and password_text != "":
                                pin_text_conversion = Authentication.number_letter_conversion(pin_text)
                                # store the account info in the authentication file
                                with open("auth.py", "a" if info_in_authfile else "w") as auth_file:
                                    app.user = Authentication(first_name_text, last_name_text, pin_text, password_text, 0)
                                    
                                    auth_file.write("\n")
                                    auth_file.write(
                                        pin_text_conversion + " = " + str(app.user.user))
                                home_screen()
                            else:
                                not_filled_fields = True
                        if show_password_rect.collidepoint(event.pos):
                            password_visible = not password_visible


                elif event.type == pygame.KEYDOWN:
                    if first_name_input_active:
                        if event.key == pygame.K_BACKSPACE:
                            first_name_text = first_name_text[:-1]
                        else:
                            if event.unicode.isalpha() and len(first_name_text) < 8:
                                # Capitalize only the first letter if the string is empty
                                if len(first_name_text) == 0:
                                    first_name_text += event.unicode.capitalize()
                                else:
                                    # Add the rest of the letters in lowercase
                                    first_name_text += event.unicode.lower()
                    elif last_name_input_active:
                        if event.key == pygame.K_BACKSPACE:
                            last_name_text = last_name_text[:-1]
                        else:
                            if event.unicode.isalpha() and len(last_name_text) < 8:
                                # Capitalize only the first letter if the string is empty
                                if len(last_name_text) == 0:
                                    last_name_text += event.unicode.capitalize()
                                else:
                                    # Add the rest of the letters in lowercase
                                    last_name_text += event.unicode.lower()
                    allowed_symbols = ["@", "$", "#", "!", "&", "*"]
                    if password_input_active:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                            visible_password = visible_password[:-1]
                        else:
                            if (event.unicode.isalnum() or event.unicode in allowed_symbols) and len(password_text) < 8:
                                password_text += event.unicode
                                # for privacy
                                visible_password += "*"



                    elif pin_input_active:
                        if event.key == pygame.K_BACKSPACE:
                            pin_text = pin_text[:-1]
                        else:
                            if event.unicode.isnumeric() and len(pin_text) < 4:
                                pin_text += event.unicode

            screen.fill(background)

            # draw rectangles
            pygame.draw.rect(screen, first_name_rect_outline_color,
                            (first_name_rect_x, first_name_rect_y, first_name_rect_width, first_name_rect_height), 2)
            pygame.draw.rect(screen, last_name_rect_outline_color,
                            (last_name_rect_x, last_name_rect_y, last_name_rect_width, last_name_rect_height), 2)
            pygame.draw.rect(screen, password_rect_outline_color,
                            (password_rect_x, password_rect_y, password_rect_width, password_rect_height), 2)
            pygame.draw.rect(screen, pin_rect_outline_color, (pin_rect_x, pin_rect_y, pin_rect_width, pin_rect_height), 2)
            # first name text in the rectangle
            first_name_text_show = font.render(first_name_text, True, (0, 0, 0))
            first_name_text_rect = first_name_text_show.get_rect(
                center=(first_name_rect_x + first_name_rect_width // 2, first_name_rect_y + first_name_rect_height // 2))
            screen.blit(first_name_text_show, first_name_text_rect)

            # last name text in the rectangle
            last_name_text_show = font.render(last_name_text, True, (0, 0, 0))
            last_name_text_rect = last_name_text_show.get_rect(
                center=(last_name_rect_x + last_name_rect_width // 2, last_name_rect_y + last_name_rect_height // 2))
            screen.blit(last_name_text_show, last_name_text_rect)

            # pin text in the rectangle
            pin_text_show = font.render(pin_text, True, (0, 0, 0))
            pin_text_rect = pin_text_show.get_rect(
                center=(pin_rect_x + pin_rect_width // 2, pin_rect_y + pin_rect_height // 2))
            screen.blit(pin_text_show, pin_text_rect)

            # Draw Show Password button
            pygame.draw.rect(screen, show_password_color, show_password_rect)
            screen.blit(show_password_text, show_password_text_rect)

            # Draw password text based on visibility
            password_text_show = font.render(password_text if password_visible else visible_password, True, (0, 0, 0))
            password_text_rect = password_text_show.get_rect(
                center=(password_rect_x + password_rect_width // 2, password_rect_y + password_rect_height // 2))
            screen.blit(password_text_show, password_text_rect)
            # text and show info

            first_name = font.render("First Name", True, (0, 0, 0))
            screen.blit(first_name, (198, 160))

            last_name = font.render("Last Name", True, (0, 0, 0))
            screen.blit(last_name, (198, 360))

            pin = font.render("PIN", True, (0, 0, 0))
            screen.blit(pin, (98, 560))

            password = font.render("Password", True, (0, 0, 0))
            screen.blit(password, (298, 560))

            sign_up = font.render("Let's Get Started!", True, (0, 0, 0))
            # instuctions_text = paragraph_font.render("Create an account to play!!", True, (169, 169, 169))
            # screen.blit(instructions_text, (125, 50))
            screen.blit(sign_up, (205, 13))

            screen.blit(back_button_image, (0, 0))
            screen.blit(forward_button_image, (600, 600))
            if not_filled_fields:
                if first_name_text == "":
                    first_name_rect_outline_color = (255, 0, 0)
                    txt1 = font.render("! Enter first name", True, (255, 0, 0))
                    screen.blit(txt1, (198, 260))
                if last_name_text == "":
                    last_name_rect_outline_color = (255, 0, 0)
                    txt2 = font.render("! Enter last name", True, (255, 0, 0))
                    screen.blit(txt2, (198, 460))
                if len(pin_text) < 4:
                    pin_rect_outline_color = (255, 0, 0)
                    txt3 = font.render("! Enter 4 letter PIN", True, (255, 0, 0))
                    screen.blit(txt3, (18, 660))
                if password_text == "":
                    txt4 = font.render("! Enter password", True, (255, 0, 0))
                    screen.blit(txt4, (298, 660))
                    password_rect_outline_color = (255, 0, 0)

            pygame.display.flip()
            # control fps
            clock.tick(app.fps)


    def access_screen():
        # sign up and login button dimensions
        background = (255, 255, 255)
        sign_up_rect = pygame.Rect(150, 200, 150, 50)
        sign_up_color = ("#00CED1")
        sign_up_text = font.render("Sign Up", True, (255, 255, 255))
        sign_up_text_rect = sign_up_text.get_rect(center=sign_up_rect.center)

        login_rect = pygame.Rect(400, 200, 150, 50)
        login_color = ("#87CEEB")
        login_text = font.render("Login", True, (255, 255, 255))
        login_text_rect = login_text.get_rect(center=login_rect.center)
        # main loop
        run = True
        while run:
            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # exit code
                    run = False
                    pygame.quit()  # clear stop running code
                    #exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if sign_up_rect.collidepoint(event.pos):
                        sign_up_screen()
                    if login_rect.collidepoint(event.pos):
                        login_screen()
            screen.fill(background)
            question_text = font.render("Login or Sign up?", True, (0, 0, 0))
            # show objects
            pygame.draw.rect(screen, sign_up_color, sign_up_rect)
            screen.blit(sign_up_text, sign_up_text_rect)

            pygame.draw.rect(screen, login_color, login_rect)
            screen.blit(login_text, login_text_rect)

            screen.blit(question_text, (50, 50))
            pygame.display.flip()
            # control fps
            clock.tick(app.fps)


    # welcome the user
    def welcome_screen():
        # define background
        background = ("#72A0C1")

        # main loop
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # exit code
                    run = False
                    pygame.quit()  # clear stop running code
                    #exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    access_screen()
            screen.fill(background)
            welcome_text = font.render("Rapid Math Racing", True, (255, 255, 255))
            start_text = paragraph_font.render("Click to start", True, (255, 255, 255))
            screen.blit(start_text, (250, 250))
            screen.blit(welcome_text, (50, 50))
            pygame.display.flip()
            # control fps
            clock.tick(app.fps)
    # for test
    welcome_screen()
    await asyncio.sleep(0)
asyncio.run(main())