#!/usr/bin/env python3
"""
Sequential ROS 2 bag player.

Given a directory that contains one or more rosbag2 recordings
(each bag is a *sub‑directory* with a `metadata.yaml` file inside),
the script plays them one after another in lexical order.

Usage:
    python3 play_bag_folder.py /path/to/bag_folder   # default playback
    python3 play_bag_folder.py /path/to/bag_folder --loop --rate 2.0

Author: (your name)
"""

import argparse
import signal
import subprocess
import sys
from pathlib import Path
from typing import List


def find_bags(folder: Path) -> List[Path]:
    """
    Return a sorted list of bag directories inside *folder*.
    A directory is considered a bag if it contains 'metadata.yaml'.
    """
    bags = [p for p in folder.iterdir()
            if p.is_dir() and (p / "metadata.yaml").exists()]
    return sorted(bags)


def play_bag(bag_path: Path, extra_args: List[str]) -> int:
    """
    Launch `ros2 bag play <bag_path>` with any additional CLI arguments.
    Returns the exit code from ros2.
    """
    cmd = ["ros2", "bag", "play", str(bag_path)] + extra_args
    print(f"\n▶️   Playing bag: {bag_path}")
    print(f"    Command: {' '.join(cmd)}")

    # Use subprocess so we can wait until playback finishes (or Ctrl‑C)
    proc = subprocess.Popen(cmd)

    try:
        return proc.wait()
    except KeyboardInterrupt:
        print("Interrupted! Stopping current playback…")
        proc.send_signal(signal.SIGINT)
        proc.wait()
        return 130  # POSIX exit code for Ctrl‑C


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Play every rosbag in a folder, sequentially."
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="Path containing rosbag2 directories."
    )
    parser.add_argument(
        "--loop", action="store_true",
        help="Pass --loop to ros2 bag play (replays each bag endlessly until Ctrl‑C)."
    )
    parser.add_argument(
        "--rate", type=float, default=None,
        help="Playback rate multiplier (passed to --rate of ros2 bag play)."
    )
    parser.add_argument(
        "--start-paused", action="store_true",
        help="Start playback in a paused state."
    )

    args = parser.parse_args()

    if not args.folder.exists() or not args.folder.is_dir():
        parser.error(f"Folder {args.folder} does not exist or is not a directory.")

    bags = find_bags(args.folder)
    if not bags:
        parser.error(f"No rosbag2 recordings found in {args.folder}")

    # Assemble extra ros2‑bag‑play arguments
    extra = []
    if args.loop:
        extra.append("--loop")
    if args.rate:
        extra += ["--rate", str(args.rate)]
    if args.start_paused:
        extra.append("--start-paused")

    for bag in bags:
        exit_code = play_bag(bag, extra)
        if exit_code != 0:
            print(f"Bag {bag} exited with code {exit_code}. Aborting sequence.")
            sys.exit(exit_code)

    print("\n✅  Finished playing all bags!")


if __name__ == "__main__":
    main()
