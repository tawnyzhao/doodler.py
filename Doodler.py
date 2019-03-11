# This is a simple drawing program.
# Features include:
#  Smooth lines
#  Setting custom thickness and colors
#  Random color and thickness modes
#  Current color and thickness displays
#  Multiple backgrounds
#  Adding custom backgrounds
#  Undo and clear button
#  Pausable background music 

# Written by Tony Zhao, 07-03-2018.

# Import statements
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
import random

CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 768

# Used for printing colors
UPPERCASE_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# List of default backgrounds
url_list = ["https://wallpapercave.com/wp/ucwC6G9.png",
            "http://www.creativehdwallpapers.com/uploads/large/background/pink-background-designs-wallpaper.jpg",
            "https://www.desktopbackground.org/p/2011/09/30/274081_uchiha-sasuke-naruto-anime-wallpapers-anime-hd-wallpapers_1600x1200_h.jpg",
            "https://img00.deviantart.net/48e1/i/2015/204/9/4/beach_anime_background__night__by_rianez3-d92ix3x.jpg",
            "https://images2.alphacoders.com/242/thumb-1920-2420.jpg",]
            
# Load images and sets initial background
background_list = []
for url in url_list:
  background_list.append(simplegui.load_image(url))
index = 0
background = background_list[index]

# Loads music and plays music
music = simplegui.load_sound("http://66.90.93.122/ost/mii-channel/blnabqdr/002%20-%20Kazumi%20Totaka%20-%20Mii%20Plaza.mp3")
music.play()
sound = True

# Wait until image loads
while background.get_width() == 0:
    pass

# Initialize global variables 
# Use all capital letters for constants
dots = []
lines = []
thickness = 10
color = "Black"
# Used for random color mode 
possible_colors = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenRod', 'DarkGray', 'DarkGrey', 'DarkGreen', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DimGrey', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod', 'Gray', 'Grey', 'Green', 'GreenYellow', 'HoneyDew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey', 'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquaMarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'RebeccaPurple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White','WhiteSmoke', 'Yellow', 'YellowGreen']
random_colors = False
random_thickness = False
color_name = color
# Used for drawing lines
prev_position = False

# Definition of Dot class
# Should have thickness, color and location attributes
class Dot:
    def __init__(self, thickness, color, location):
        self.thickness = thickness
        self.color = color
        self.location = location
    def draw(self, canvas):
        canvas.draw_circle(self.location, self.thickness, 1, self.color, self.color)
    def getcolor(self):
        return self.color

# Line class to smooth drawing
class Line:
        def __init__(self, location1, location2, thickness, color):
                self.loc1 = location1
                self.loc2 = location2
                self.thickness = thickness
                self.color = color 
        def draw(self, canvas):
                canvas.draw_line(self.loc1, self.loc2, self.thickness, self.color)
            
# Handler for clear button
def clear_handler():
    global dots, lines
    dots = []
    lines = []
    
# Handler to change thickness    
def thickness_handler(text_input):
    global thickness
    if int(text_input) < 500:
        thickness = int(text_input)
    else:
        thickness = 500

# Handler to change color    
def color_handler(text_input):
    global color, color_name
    color = text_input
    color_name = color

# Handler to set background 
def background_handler():
    global index, background
    if index < len(url_list) - 1:
        index += 1
    else:
        index = 0
    background = background_list[index]

# Handler to change color mode
def colormode_handler():
    global random_colors
    if random_colors == True:
        random_colors = False
    else:
        random_colors = True

# Handler to change thickness mode
def thicknessmode_handler():
    global random_thickness
    if random_thickness == True:
        random_thickness = False
    else:
        random_thickness = True

# Handler for undo
def undo_handler():
    global lines, dots
    # Removes the last 10 dots and lines created
    lines = lines[:-10]
    dots = dots[:-10]

# Function to format color string with spaces
def split_color(color):
    result = ""
    for i in range(len(color)):
        if color[i] in UPPERCASE_ALPHABET:
            result += " "
            result += color[i]
        else:
            result += color[i]
    return result

# Handler to add user backgrounds
def background_add(text_input):
    global url_list
    url_list.append(text_input)
    background_list.append(simplegui.load_image(url_list[-1]))

# Handler to play and pause music
def music_handler():
    global sound
    if sound:
        music.pause()
        sound = False
    else:
        music.play()
        sound = True
        
# Mouse click handler
# Adds a dot at that position using the current 
# thickness and color settings

def mouse(position):
    global color, color_name, thickness
    if random_colors and random_thickness:
        thickness = random.randint(1,40)
        dots.append(Dot(thickness, random.choice(possible_colors), position))
        color = dots[-1].getcolor()
        color_name = split_color(color)
    elif random_colors:
        dots.append(Dot(thickness, random.choice(possible_colors), position))
        color = dots[-1].getcolor()
        color_name = split_color(color)
    elif random_thickness:
        thickness = random.randint(1,40)
        dots.append(Dot(thickness, color, position))
    else:
        dots.append(Dot(thickness, color, position))
 
def mouse_click(position):
    mouse(position)
    global prev_position
    # Upon mouse release, stops connecting lines to dots
    prev_position = False
def mouse_drag(position):
    mouse(position)
    global lines, prev_position
    if prev_position == False:
      prev_position = position
    # Creates lines to connect dots
    else:
      lines.append(Line(prev_position, position, 2*thickness, color))
      prev_position = position
        
# Handler to draw on canvas
def draw(canvas):
    canvas.draw_image(background,
                      (CANVAS_WIDTH/2, CANVAS_HEIGHT/2),
                      (CANVAS_WIDTH, CANVAS_HEIGHT),
                      (CANVAS_WIDTH/2, CANVAS_HEIGHT/2),
                      (CANVAS_WIDTH, CANVAS_HEIGHT))
    
    for dot in dots:
        dot.draw(canvas)
    for line in lines:
        line.draw(canvas)
    
    # Updates labels
    current_thickness.set_text("Current thickness is " + str(thickness))
    current_thickness_mode.set_text("Random Thickness Mode: " + str(random_thickness))
    current_color.set_text("Current color is " + color_name)
    current_color_mode.set_text("Random Color Mode (works best with a thin thickness): " + str(random_colors))
    

# Create a frame 
frame = simplegui.create_frame("Doodler", CANVAS_WIDTH, CANVAS_HEIGHT)

# Create buttons & text inputs
# Assign callbacks to handler functions
frame.set_mouseclick_handler(mouse_click)
frame.set_mousedrag_handler(mouse_drag)

frame.add_input("Thickness? (1 - 500 px)", thickness_handler, 200)
current_thickness = frame.add_label("The thickness is " + str(thickness))
frame.add_label("")

frame.add_input("Colour?", color_handler, 200)
current_color = frame.add_label("Current color is " + color_name)
frame.add_label("")

frame.add_button("Color Mode", colormode_handler)
current_color_mode = frame.add_label("Random Color Mode (works best with a thin thickness): " + str(random_colors))
frame.add_label("")

frame.add_button("Thickness Mode", thicknessmode_handler)
current_thickness_mode = frame.add_label("Random Thickness Mode: " + str(random_thickness))
frame.add_label("")

frame.add_input("Add your own Background (URL):", background_add, 200)
frame.add_button("Next Background", background_handler)
frame.add_label("")

frame.add_button("Undo", undo_handler)
frame.add_label("")

frame.add_button("Clear", clear_handler)
frame.add_label("")
frame.add_label("")
frame.add_label("")

frame.add_button("Toggle Music", music_handler)
frame.add_label("")

# Start the frame
frame.set_draw_handler(draw)
frame.start()

