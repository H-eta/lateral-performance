import sys
import os
from main import app as application

sys.path.insert(0, os.path.dirname(__file__))

sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'libs'))