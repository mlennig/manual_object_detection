import math
from PIL import Image
import os
import glob

class RPi_ImageProcessing:
    IMAGE_SCALING_FACTOR = 4                        # Image size is reduced by this factor
    
    def __init__(self, images_dir: str):
        # Member variables (object properties)
        self.sensor_length_x: float = 4.5 / 1000   
        self.sensor_length_y: float = 6.2 / 1000
        self.focal_length: float = 5.64 / 1000      # Focal length multiplier    
        self.images_dir = images_dir
        self.CM_PER_PIXEL = 1.18                    # To be modifed based on mission planner information
        self.M_PER_PIXEL = self.CM_PER_PIXEL / 100. # Meters per pixel of image
        self.current_image: Image = None
        self.current_x_len = None
        self.current_y_len = None
        

    def calculate_image_scale(self, altitude: float) -> (float, float):
        """
        Calculate scale of x and y axis of image based on camera parameters and altitude. Produces a tuple of dimensions

        :param altitude: height in meters
        :return: (width, height)
        """
        # width, height are dimensions of the area in the picture, in meters
        width = altitude / self.focal_length * self.sensor_length_x
        height = altitude / self.focal_length * self.sensor_length_y

        return width, height

    def calculate_gps_position(self, lat: float, lon: float, dx: float, dy: float, heading: float) -> (float, float):
        """
        Calculate new GPS latitude and longitude based on a displacement of dx and dy meters

        :param lat: Initial latitude
        :param long: Initial longitude
        :param dx: displacement in X
        :param dy: displacement in Y
        :return: (ph2, lambda2), the lat, lon of the point clicked, in DEGREES
        """
        R: float = 6378137.                     # Radius of the earth in meters
        phi1 = math.radians(lat)                # Latitude of center of GoPro photo, in RADIANS
        lambda1 = math.radians(lon)             # Longitude of center of GoPro photo, in RADIANS
        delta = math.sqrt(dx**2 + dy**2) / R    # Angular distance d/R; d being the distance travelled, R the earth's radius
        theta = self.calculate_bearing(dx, dy, math.radians(heading))   # Bearing of the clicked point in RADIANS, clockwise from North
        
        # Latitude of point clicked in RADIANS
        phi2 = math.asin(math.sin(phi1) * math.cos(delta) + math.cos(phi1) * math.sin(delta) * math.cos(theta))
        
        # Longitude of point clicked in RADIANS
        y = math.sin(theta) * math.sin(delta) * math.cos(phi1)
        x = math.cos(delta) - math.sin(phi1) * math.sin(phi2)
        lambda2 = lambda1 + math.atan2(y, x) 
        
        # Return lat, lon in DEGREES of point clicked
        return math.degrees(phi2), math.degrees(lambda2)

    def calculate_displacement(self, x, y, width, height, imageWidthMeters, imageHeightMeters) -> (float, float):
        """
        Calculates the displacement in meters from center based on (x,y) pixel placement

        :param x: x pixel position
        :param y: y pixel position
        :return: (dx, dy)
        """
        # Width, height are the pixel dimensions of the image 
        # width, height = self.current_image.size
        
        """(x - the midpoint (of width)) * the distance per pixel value"""
        # self.current_x_len, self.current_y_len are the dimensions of the area
        # in the picture, in meters         
        dx = (x - width / 2.) * (imageWidthMeters / width)
        dy = (y - height / 2.) * (imageHeightMeters / height)

        return dx, dy
    
    def calculate_bearing(self, dx, dy, heading):
        # Calculate the bearing, in RADIANS, required to go from where the
        # drone took the picture to the click point  
        
        def calculate_relative_bearing(dx, dy):
            # Compute the required bearing, in RADIANS, relative to the heading 
            # the drone had when it took the picture 
            if(dx > 0):
                theta = math.pi/2. - math.atan(dy/dx)
            elif(dx < 0):
                theta = 3 * math.pi/2. - math.atan(dy/dx)
            else:
                if(dy > 0):
                    theta = math.pi/2
                elif(dy < 0):
                    theta = -math.pi/2
                else:
                    theta = 0
            return theta
        
        # Bearing = (theta + heading) % 2pi
        theta = calculate_relative_bearing(dx, dy)
        return (theta + heading) % (2. * math.pi)
    
        
    
    


