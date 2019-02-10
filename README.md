# Obstacle-Avoiding-Bot
This is simple program written in python to simulate a bot having proximity sensors. The bot moves towards the destination with the
help of sensor stimuli. I have used pygame (a python library used to make simple 2D games) to build the interface.   

First, I built a simple interface where the user can set the start and end locations and draw obstacles using mouse clicks. 

Then I modeled the behaviour of proximity sensors.  
There are a total of 13 sensors pointing from -90 to +90 degrees with respect to the true heading angle ( T.H.A - angle from end location to start location) in steps of 15.   
There are 3 types of sensors -   
Primary sensors - (7 Nos) Pointing from -45 to +45 degrees with respect to T.H.A. Length - 10 units  
Secondary sensors - (2 Nos) Pointing at -60 and +60 degrees with respect to T.H.A. Length - 8 units  
Tertiary sensors - (4 Nos) Pointing at -90,-75,75,90 degrees with respect to T.H.A. Length - 5 units  
This was done as the the sensors at the trailing ends were causing change in heading angle unnecessarily.   

The sensors have a default return value of 10/8/5 (depending on the type of sensor) if they do not encounter any obstacle. If there is an obstacle in it's range, it's return value reduces accordingly depending on how close the bot is to the obstacle in that direction.    
The return values of each sensor is stored in a list and a weighted mean is taken.   
Weighted mean = Sum(return value * angle of sensor) / Sum(return values).  
This weighted mean is multiplied by a scaling factor and is added to the heading angle.  
This, in short, enables the bot to turn.  
