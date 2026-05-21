#!/usr/bin/env python3
"""
Prepare images for the PreTeXt book build.
This script downloads official CC license icons (if network is available)
to update the locally committed fallback icons.
"""

import urllib.error
import urllib.request
import shutil
from pathlib import Path


# Official Creative Commons presskit icon URLs
CC_ICONS = {
    "cc.xlarge.png": "https://mirrors.creativecommons.org/presskit/icons/cc.xlarge.png",
    "by.xlarge.png": "https://mirrors.creativecommons.org/presskit/icons/by.xlarge.png",
    "nc.xlarge.png": "https://mirrors.creativecommons.org/presskit/icons/nc.xlarge.png",
    "sa.xlarge.png": "https://mirrors.creativecommons.org/presskit/icons/sa.xlarge.png",
}

_DOWNLOAD_TIMEOUT = 30  # seconds


def try_download_cc_icons(target_dir: Path) -> int:
    """Try to download official CC license icons. Returns number downloaded."""
    downloaded = 0
    for filename, url in CC_ICONS.items():
        target_file = target_dir / filename
        try:
            urllib.request.urlretrieve(url, str(target_file))
            downloaded += 1
            print(f"  Downloaded: {filename}")
        except (urllib.error.URLError, OSError) as e:
            print(f"  Warning: Could not download {filename} from {url}: {e}")
            print(f"  Using committed fallback icon for {filename}")
    return downloaded


def main():
    script_dir = Path(__file__).parent
    pretext_images_dir = script_dir / "pretext" / "assets" / "images"

    print("Preparing images for PreTeXt book...")

    # Try to download official CC license icons to replace fallback versions
    print("\nAttempting to download official CC license icons...")
    downloaded = try_download_cc_icons(pretext_images_dir)
    if downloaded == len(CC_ICONS):
        print(f"  Successfully downloaded all {downloaded} CC license icons.")
    elif downloaded > 0:
        print(f"  Downloaded {downloaded}/{len(CC_ICONS)} CC license icons.")
    else:
        print("  Could not download CC icons - using committed fallback icons.")

    # Check if ImageMagick convert is available (for future EPS conversion)
    convert_available = shutil.which("convert") is not None
    if convert_available:
        print("\nImageMagick found (available for future EPS-to-PNG conversion).")

    print("\nComplete!")
    return 0


if __name__ == "__main__":
    exit(main())
