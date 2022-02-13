#!/usr/bin/env bash

if [[ -d 'vendor' ]]; then 
    python -m venv vendor;
fi

source vendor/bin/activate;
pip install -r requirements.txt;
deactivate;