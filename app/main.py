import sys
import os
import zlib
import hashlib

def main():
    # print("Logs from your program will appear here!")
    
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
        if plummbing_flag == "p":
            blob_id = sys.argv[3]
            blob_dir = "".join(blob_id[:2])
            path = ".git/objects/" + blob_dir + "/" + "".join(blob_id[2:])
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
                a = ""
                for letter in ans[-1]:
                    v = ord(letter) - 97 
                    if v >= 0 and v < 26:
                        a += letter
                ans[-1] = a
                print(" ".join(ans), end="")
    elif command == "hash-object":
        plummbing_flag = sys.argv[2]
        file_name = sys.argv[3]
        with open(file_name, "r") as f:
            content = f.read()
            blob_header = b"blob " + str(len(content)) + "\\0" + content
            hash_content = hashlib.sha1(blob_header).hexdigest()
            compressed_blob = zlib.compress(hash_content)
            directory_path = ".git/objects" +"/" + hash_content[2:]
            os.mkdir(directory_path)
            file_path = directory_path + "/" + file_name
            with open(file_path, "w") as f:
                f.write(compressed_blob)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
