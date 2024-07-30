import sys
import os
import zlib

def main():
    print("Logs from your program will appear here!")
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        plummbing_flag = sys.argv[2]
        blob_id = sys.argv[3]
        path = ".git/objects/" + "".join(blob_id[:2])
        blob_object = open(path)
        decompress_blob = str(zlib.decompress(blob_object))
        _, content = decompress_blob.split(" ")
        contents = content.split("\0")
        print(contents[1])
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
