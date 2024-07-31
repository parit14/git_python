import sys
import os
import zlib
import hashlib


class TreeObject:
    def __init__(self):
        self.tree_objects = []
        self.files = []

def writeTree(direc: str) -> str:
    names = sorted([name for name in os.listdir(direc)])
    sha_hash = bytes()
    for name in names:
        if name != ".git":
            p = direc + "/" + name
            if os.path.isfile(p):
                encoded_str = "10064 " + name + "\0" 
                sha_hash+= (encoded_str.encode())
                file_hash = writeBlob(p, name)
                file_sha_hash = int.to_bytes(int(file_hash, base=16), length=20, byteorder="big")
                sha_hash+=file_sha_hash
            else:
                encoded_str = "40000 " + name + "\0" 
                sha_hash+= (encoded_str.encode())
                file_hash = writeTree(p)
                file_sha_hash = int.to_bytes(int(file_hash, base=16), length=20, byteorder="big")
                sha_hash+=file_sha_hash
    tree_hash = ("tree " + str(len(sha_hash)) + "\0").encode() + sha_hash
    sha = hashlib.sha1(tree_hash).hexdigest()
    direc_path = ".git/objects" +"/" + sha[:2]
    os.mkdir(direc_path)
    file_path = direc_path + "/" + sha[2:]
    # print(direc_path, file_path)
    with open(file_path, "wb") as f:
        f.write(zlib.compress(tree_hash))
    return sha


def writeBlob(path: str, name: str) -> str:
    with open(path, "r") as f:
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
    return hash_str

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
            vals = decompressed_tree.split(" ")
            names = []
            for val in vals[2:]:
                val_split = val.split("\\x")
                names.append(val_split[0])
            for n in sorted(names):
                print(n)
    elif command == "write-tree":
        print(writeTree("./"))
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()