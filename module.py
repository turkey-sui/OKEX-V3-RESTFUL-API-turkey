import os, sys

def determine_path ():
    """Borrowed from wxglade.py"""
    try:
        root = __file__
        if os.path.islink (root):
            root = os.path.realpath (root)
        return os.path.dirname (os.path.abspath (root))
    except:
        print "I'm sorry, but something is wrong."
        print "There is no __file__ variable. Please contact the author."
        sys.exit ()
        
def start ():
    print "module is running"
    print determine_path ()
    print "My various data files and so on are:"
    files = [f for f in os.listdir(determine_path () + "/things")]
    print files
    
if __name__ == "__main__":
    print "Decide what to do"