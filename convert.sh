#!/bin/bash

# Directory containing the ROS1 bag files
INPUT_DIR="/media/uav/T7/data/stabilizer/frick_park_path2_mar14/path2/2025_03_14/collect_01/raw"
# Directory to save converted ROS2 bag files
OUTPUT_DIR="/media/uav/T7/data/stabilizer/frick_park_path2_mar14/path2/2025_03_14/collect_01/raw/ros2/"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Iterate over each .bag file in the input directory
for bagfile in "$INPUT_DIR"/*.bag; do
    # Get just the filename without the directory
    filename=$(basename -- "$bagfile")
    # Remove the .bag extension
    filename_noext="${filename%.*}"
    # Define output path
    output_path="$OUTPUT_DIR/$filename_noext"

    echo "Converting $bagfile to ROS2 format..."

    # Run rosbag convert (replace with the actual command you're using)
    rosbags-convert "$bagfile"

    echo "Saved to $output_path"
done

