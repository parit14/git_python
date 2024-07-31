import sys
import os
import zlib
import hashlib


class TreeObject:
    def __init__(self):
        self.tree_objects = []
        self.files = []

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
        # if plummbing_flag == "p":
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
            blob_header = bytes("blob " + str(len(content)) + "\x00" + content, 'utf-8')
            hash_content = hashlib.sha1(blob_header)
            hash_str = hash_content.hexdigest()
            compressed_blob = zlib.compress(blob_header)
            directory_path = ".git/objects" +"/" + hash_str[:2]
            os.mkdir(directory_path)
            file_path = directory_path + "/" + hash_str[2:]
            with open(file_path, "wb") as f:
                f.write(compressed_blob)
            print(hash_str)
    elif command == "ls-tree":
        plummbing_flag = sys.argv[2]
        sha_id = sys.argv[3]
        path = ".git/objects/" + "".join(sha_id[:2]) + "/" + "".join(sha_id[2:])
        with open(path, "rb") as f:
            decompressed_tree = str(zlib.decompress(f.read()))
            vals = decompressed_tree.split("\x00")
            print(vals)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()