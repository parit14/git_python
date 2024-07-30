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
        blob_dir = "".join(blob_id[:2])
        path = ".git/objects/" + blob_dir + "/" + "".join(blob_id[2:])
        blob_object = open(path)
        with open(path, "rb") as f:
            decompress_blob = str(zlib.decompress(f.read()))
            vals = decompress_blob.split(" ")
            ans = []
            for idx, val in enumerate(vals):
                if "\\x00" in val:
                    vs = val.split("\\x00")
                    ans.append(vs[-1])
                    ans += vals[idx+1:]
                    break
            ans[-1].strip("'")
            print(" ".join(ans))
    
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
