#!/bin/sh
echo "   *** Script made by lordcodes"
python -m pip install -r requirements.txt --no-index --find-links file:///tmp/packages
python run.py
