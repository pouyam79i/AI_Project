# Debug Mode
# It will show debug msg in console if the mode is true!
debug_mode = True

# Helps handling debug messages
class MyDebugger:

    def __init__(self):
        self.debug_location = "Unknown Location!"
        self.debug_msg = "No MSG!"


    def set_defalt_location(self, debug_location):
        self.debug_location = debug_location

    def set_defalt_msg(self, debug_msg):
        self.debug_msg = debug_msg

    # Raise a debug flag
    def flag(self, debug_location=None, debug_msg=None):
        
        if debug_mode is True:
            
            if debug_msg is None:
                debug_msg = self.debug_msg

            if debug_location is None:
                debug_location = self.debug_location

            print("#DEBUG @ {} : {}.".format(str(debug_location), str(debug_msg)))
