#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Usage: $0 <image-file>"
    exit 1
fi

# Create a 64x64 thumbnail
convert "$1" -resize 64x64 thumb.png

# Convert it to base64 and copy to clipboard
encoded_image=$(base64 -i thumb.png)
echo "data:image/png;base64,$encoded_image" | xclip -selection clipboard

# Clean up
rm thumb.png

#echo "base64 image copied to clipboard."
