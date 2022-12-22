# dotkeep-fuse
## What is this
This tool is for helping manuplating directories on Google Drive behind union using rclone, which allows having many files with the same name.

You can create all the necessary directories first on singlular drive remote, and upload 750GB+ of files by using a union remote with many SAs behind.

## How to use
```bash
pip install fuse-python

git clone https://github.com/KoushinRip-OSS/dotkeep-fuse
cd dotkeep-fuse
python3 dotkeep.py -o root=<path to source in full path> -o ro <mountpoint>

rclone copy --include=.keep <mountpoint> gdrive1:backups/
rclone copy <source path> gdrive-union:backups/
```
