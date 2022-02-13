#!/usr/bin/env bash

source vendor/bin/activate;
pip freeze > requirements.txt;
deactivate;