#!/bin/bash

SCRIPT_DIR="/opt/steghide-mkv"
VENV_DIR="$SCRIPT_DIR/venv"

# Activate the virtual environment installed by the Makefile
source "$VENV_DIR/bin/activate"

if [[ "$1" == "extract" ]]; then
    if [[ "$2" == "-f" ]]; then
        python3 "$SCRIPT_DIR/steghide-extract-mkv.py" "$4" "$3"
    else
        python3 "$SCRIPT_DIR/steghide-extract-mkv.py" "$2"
    fi

elif [[ "$1" == "embed" ]]; then
    if [[ "$2" == "-f" ]]; then
        python3 "$SCRIPT_DIR/steghide-mkv.py" "$4" "$5" "$3"
    else
        python3 "$SCRIPT_DIR/steghide-mkv.py" "$2" "$3"
    fi

else
    echo "steghide-mkv supports only embed and extract attributes."
    echo "Usage:"
    echo "  steghide-mkv embed <input_video> <secret_file>"
    echo "  steghide-mkv embed -f <output_file> <input_video> <secret_file>"
    echo "  steghide-mkv extract <video_with_hidden_data>"
    echo "  steghide-mkv extract -f <output_file> <video_with_hidden_data>"
    echo ""
    echo "If you want to specify the output filename, use the -f flag."
fi

deactivate
