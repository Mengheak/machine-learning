# Practical Linux on Kali · Student workbook

Work through A1–A25, B1–B15, then C1–C19. The numbered extension labs and projects follow. Some tasks revisit an earlier command with less guidance. For each lab, predict the result, run it, and record one observation. The checks are your marking guide.

## Before you begin

Use a normal user in your Kali VM. Take a VM snapshot before account, disk, or firewall labs. Commands below run inside Linux. A line starting with `#` explains the command below it. A block marked **file contents** goes in a file. Use `nano filename` to open the editor, Ctrl+O then Enter to save, and Ctrl+X to leave. Start a Bash session for these labs so examples work even when your login shell is Zsh.

```bash
# Start Bash in this terminal. Type exit to leave it later.
bash
# Build the course folders. ~ means your home directory, -p makes missing parents, and braces expand into several names.
mkdir -p ~/linux-lab/{notes,data,scripts,backups,restore,reports,run}
# Switch to the practice workspace. Repeat this after opening a new terminal.
cd ~/linux-lab
```

**Reading the examples.** A space separates a command from its arguments. Quotes keep a path containing spaces together. `$name` expands a variable. `$(command)` substitutes a command's output. A pipe (`|`) sends output to the next command. `>` creates or replaces a file, `>>` appends, and `<` reads input from a file. `2>` redirects errors. `--` ends option processing for commands that support it. A command may succeed silently. Run `echo $?` immediately afterward to print its exit status (usually 0 for success). `sudo` runs a command with elevated privileges. Use it only on the marked steps. For multiline examples, paste the whole block. A line ending in a backslash continues on the next line.

**Where to work.** A, C, and most extension labs run on one VM. B6 introduces the server for SSH. Use a second VM on a private lab network for a realistic transfer and recovery test. A one-VM practice option is included there.

## A · Linux fundamentals and administration

### A1 · Identify your system

Find out who and where you are.

```bash
# Print your effective username and current directory, respectively.
whoami
pwd

# Print the machine name, then the kernel release.
hostname
uname -r

# Read the distribution's identification file.
cat /etc/os-release

# Print the configured login shell, then the current shell process's command name. $$ is its PID.
echo "$SHELL"
ps -p "$$" -o comm=
```

**Assignment and check.** Record username, distribution, kernel, and current shell. Explain which program interprets your commands.

### A2 · Navigate

Start at ~/linux-lab.

```bash
# Create a nested project tree.
mkdir -p projects/website/assets

# Create an empty file, or update its timestamp if it exists.
touch notes/day1.txt

# List files, then include hidden names (-a) and details (-l).
ls
ls -la

# Enter notes, move up one level, go home, then return to the previous directory.
cd notes
cd ..
cd ~
cd -
```

**Assignment and check.** Use pwd after each move. Reach assets once using a path starting with / and once using a relative path.

### A3 · Manage files

Work from ~/linux-lab.

```bash
# Write one line. The newline escape ends the line.
printf 'My first Linux note\n' > notes/start.txt

# Copy the note, then rename only the copy.
cp notes/start.txt notes/start-copy.txt
mv notes/start-copy.txt notes/renamed.txt

# Make a disposable directory and file.
mkdir -p temporary
touch temporary/test.txt

# Remove that file, then remove its empty parent.
rm temporary/test.txt
rmdir temporary
```

**Assignment and check.** Create three notes, copy them to backups, rename and remove one original. List backups to prove all three copies remain.

### A4 · Read and edit

Create a five-line file.

```bash
# Print each argument on a separate line.
printf '%s\n' Linux Kali Terminal Files Permissions > notes/topics.txt

# Print the whole file, first two lines, last two lines, then its newline count.
cat notes/topics.txt
head -n 2 notes/topics.txt
tail -n 2 notes/topics.txt
wc -l notes/topics.txt

# Edit the file, then browse it page by page. Press q to leave less.
nano notes/topics.txt
less notes/topics.txt
```

**Assignment and check.** Add five topics. Display only the last three and confirm the file now has ten lines.

### A5 · Find help

Practice locating an option independently.

```bash
# Open the ls manual. Type /time then Enter to search, n for the next match, q to quit.
man ls

# Print built-in usage information for ls.
ls --help

# Ask Bash how it resolves each command.
type cd
type ls
```

**Assignment and check.** Use the manual to construct a listing with sizes in human-readable units and newest changes first. Try ls -lht to check.

### A6 · Count with pipes

Build a small frequency table.

```bash
# Create a five-line dataset.
printf '%s\n' apple banana apple orange banana > data/fruit.txt

# Sort identical lines together, count consecutive matches, then sort numerically in reverse.
sort data/fruit.txt | uniq -c | sort -nr > data/fruit-counts.txt

# Read the saved counts.
cat data/fruit-counts.txt

# Create a journal, then append another line without replacing the first.
echo 'First entry' > notes/journal.txt
echo 'Second entry' >> notes/journal.txt
```

**Assignment and check.** Expect two apples, two bananas, one orange. Explain why sort precedes uniq.

### A7 · Search

Separate matching names from matching contents.

```bash
# Find Linux in one file and show line numbers.
grep -n 'Linux' notes/topics.txt

# Search all files under notes recursively, ignoring letter case.
grep -ri 'linux' notes

# Search below the current directory for regular files matching the quoted pattern.
find . -type f -name '*.txt'

# Find directories, then files modified less than one day ago.
find . -type d
find . -type f -mtime -1
```

**Assignment and check.** Find names containing day. Explain who interprets the quoted wildcard in the find command.

### A8 · Analyze scores

Use this simple CSV fixture. The fields contain no embedded commas.

```bash
# Feed four data rows and a header to cat, ending at EOF, and save them as a file.
cat > data/scores.csv <<'EOF'
name,team,score
Alice,blue,80
Bob,red,65
Carol,blue,95
David,red,70
EOF

# Split at commas and print field 1.
cut -d, -f1 data/scores.csv

# Skip the header (NR > 1). Print names and scores where field 3 is at least 80.
awk -F, 'NR > 1 && $3 >= 80 {print $1, $3}' data/scores.csv

# Accumulate scores and a row count, then print their quotient.
awk -F, 'NR>1 {s+=$3; n++} END {if(n) print s/n}' data/scores.csv
```

**Assignment and check.** Add a condition on field 2 to calculate the blue team's average. Expect 87.5.

### A9 · Protect a note

Read the owner, group, and other permission bits.

```bash
# Write the note and inspect its initial mode.
echo 'Private practice note' > notes/private.txt
ls -l notes/private.txt

# Set owner read/write only, then display octal mode, symbolic mode and name.
chmod 600 notes/private.txt
stat -c '%a %A %n' notes/private.txt
```

**Assignment and check.** Try mode 640, then restore 600. Explain each digit using read=4, write=2, execute=1.

### A10 · Back up and restore

Use a fresh restore folder each time.

```bash
# Create (-c) a gzip-compressed (-z) archive at the filename given by -f.
tar -czf backups/notes.tar.gz notes

# List (-t) the archive's contents before extraction.
tar -tzf backups/notes.tar.gz

# Create a new empty directory and capture its name.
restored=$(mktemp -d "$HOME/linux-lab/restore/run.XXXXXX")

# Extract (-x) inside the directory passed to -C.
tar -xzf backups/notes.tar.gz -C "$restored"

# Compare directory trees recursively. Silence and exit status 0 mean equal contents.
diff -r notes "$restored/notes"
```

**Assignment and check.** Make another archive with today's date. Use date +%F to print a YYYY-MM-DD date.

### A11 · Manage processes

Start and terminate a process you own.

```bash
# List processes across users with resource details. Then inspect them interactively (q exits).
ps aux
top

# Run sleep in the background and save its PID from $!.
sleep 300 &
lab_pid=$!

# Show PID, parent PID, state, and command. jobs lists this shell's jobs.
ps -p "$lab_pid" -o pid,ppid,stat,cmd
jobs

# Send the default termination signal to this sleep process.
kill "$lab_pid"
```

**Assignment and check.** Run ps again. Explain why you saved the PID immediately after starting sleep.

### A12 · Measure storage and memory

Compare filesystem capacity with file usage.

```bash
# Show free filesystem space, workspace usage, memory, and block devices, respectively.
df -h
du -sh ~/linux-lab
free -h
lsblk

# Create a disposable 20 MiB regular file. if supplies zeros, of is the output file, bs and count set the size.
dd if=/dev/zero of=data/testfile.bin bs=1M count=20

# Measure all entries, sort by human-readable size, and show the largest five.
du -ah . | sort -hr | head -n 5

# Delete only the test file.
rm data/testfile.bin
```

**Assignment and check.** Explain why df and du report different totals.

### A13 · Inspect packages

Query the package database.

```bash
# Search for the exact package name tree, then display its metadata.
apt search '^tree$'
apt show tree

# Show Bash's installation status and list files installed by its package.
dpkg -l bash
dpkg -L bash
```

**Assignment and check.** Find Bash's installed version. Explain the difference between apt update (refresh available package lists) and apt upgrade (install available upgrades).

### A14 · Inspect services and logs

Find evidence about this boot.

```bash
# List failed units, then running service units.
systemctl --failed
systemctl list-units --type=service --state=running

# Show the latest 50 journal entries from this boot without opening a pager.
journalctl -b -n 50 --no-pager
```

**Assignment and check.** Choose a running service. Replace NAME in systemctl status NAME with it to inspect state, and in journalctl -u NAME to filter by unit. Use sudo for restricted logs. Explain running now versus enabled for startup.

### A15 · Inspect networking

Identify addresses, routes, and listeners.

```bash
# List interface addresses briefly and print the routing table.
ip -br address
ip route

# Read resolver configuration and look up a hostname using the system's configured lookup methods.
cat /etc/resolv.conf
getent hosts example.com

# List listening TCP and UDP sockets numerically.
ss -tuln
```

**Assignment and check.** Record the VM address, default gateway if present, and one listener. The loopback address 127.0.0.1 refers to the machine on which the connection is made.

### A16 · Your first Bash script

Save the following as scripts/hello.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.

# Use argument 1 if nonempty, otherwise use student.
name="${1:-student}"

# Substitute the name into %s and end with a newline.
printf 'Hello, %s!\n' "$name"
```

**Assignment and check.** Put the #!/usr/bin/env bash line first when saving the file. chmod u+x scripts/hello.sh gives the owner execute access. ./scripts/hello.sh runs the file. Try it with no argument, then with 'Linux learner'. Add username, date and hostname.

### A17 · Return meaningful exit codes

Save as scripts/check-file.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.

# If the argument count differs from one, print usage to standard error and return 2. fi closes the condition.
if [[ $# -ne 1 ]]; then
  printf 'Usage: %s FILE\n' "$0" >&2
  exit 2
fi

# Test for a regular file. Report a missing file and return 1 on failure.
if [[ -f "$1" ]]; then
  printf 'Found: %s\n' "$1"
else
  printf 'Not found: %s\n' "$1" >&2
  exit 1
fi
```

**Assignment and check.** bash scripts/check-file.sh /etc/hosts executes the script with an existing file. Repeat with a missing path, then no argument. After each run print $? and expect 0, 1, 2.

### A18 · Count lines safely

Save as scripts/count-lines.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.

# Read each NUL-terminated path without splitting or treating backslashes as escapes. find emits the matching paths; < <(...) feeds them to the loop.
while IFS= read -r -d '' file; do
  # Print the name, then count newlines using the file as standard input.
  printf '%s: ' "$file"
  wc -l < "$file"
done < <(find "$HOME/linux-lab/notes" -type f -name '*.txt' -print0)
```

**Assignment and check.** Create a note named meeting notes.txt, run the script with bash, and verify it appears once. Add a counter and print the number of files processed.

### A19 · Write backup-notes.sh

Build the script yourself using A10, A16 and A17.

```bash
# Generate a date and time suitable for a filename.
date '+%Y%m%d-%H%M%S'

# Test whether the notes directory exists. [[ ... ]] returns a status you can use in an if statement.
[[ -d "$HOME/linux-lab/notes" ]]
```

**Assignment and check.** Create a timestamped archive in backups, guard against a missing source and an existing output filename, print its path, and return failure on errors. Run twice and restore one archive into a fresh directory.

### A20 · Schedule a harmless job

Use your user crontab.

```bash
# Inspect the scheduler. If it is installed but inactive, start it.
systemctl status cron
# Run only if needed.
sudo systemctl start cron

# Open your own schedule in an editor.
crontab -e
```

**Assignment and check.** Add the entry below. The five stars match every minute, hour, day of month, month, and day of week. The absolute command prints the time; 2>&1 sends errors to the same log as normal output. After two entries, remove only this line using crontab -e.

```cron
* * * * * /usr/bin/date >> "$HOME/linux-lab/notes/cron-test.log" 2>&1
```

### A21 · Serve a local page

Use two terminals.

```bash
# Create a web directory and write its index page.
mkdir -p ~/linux-lab/web
printf '<h1>Hello from Kali</h1>\n' > ~/linux-lab/web/index.html

# Terminal 1: run Python's HTTP server on loopback port 8000, serving only the lab web directory.
python3 -m http.server 8000 --bind 127.0.0.1 --directory ~/linux-lab/web

# Terminal 2: request the page with response headers, then show the process listening on 8000.
curl -i http://127.0.0.1:8000/
ss -ltnp | grep ':8000'
```

**Assignment and check.** Request /missing for a 404. Stop the server with Ctrl+C and request / again. Explain the difference between HTTP 404 and connection refused.

### A22 · Resolve a port conflict

Repeat A21's server command in two terminals.

```bash
# Filter listening TCP sockets to the port in question and show process details.
ss -ltnp 'sport = :8000'

# Start a second server on a free port.
python3 -m http.server 8001 --bind 127.0.0.1 --directory ~/linux-lab/web
```

**Assignment and check.** Capture the original error. Request both ports with curl from another terminal, then stop both servers with Ctrl+C.

### A23 · Manage a user service

Create the unit file below.

```bash
# Create the user service directory and open the unit file for editing.
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/linux-lab-web.service
```

**Assignment and check.** Use this file. Description names the service, ExecStart runs the server (%h expands to your home), Restart retries after failure, and WantedBy identifies the target for enabling it.

```ini
[Unit]
Description=Linux lab web server
[Service]
ExecStart=/usr/bin/python3 -m http.server 8000 --bind 127.0.0.1 --directory %h/linux-lab/web
Restart=on-failure
[Install]
WantedBy=default.target
```

```bash
# Reload user unit definitions, then start and inspect your service.
systemctl --user daemon-reload
systemctl --user start linux-lab-web
systemctl --user status linux-lab-web
# Show the latest 20 journal entries for this user service.
journalctl --user -u linux-lab-web -n 20 --no-pager
```
Change the port to 8080, reload definitions, and use `systemctl --user restart linux-lab-web` to apply it. Confirm with curl. `systemctl --user stop linux-lab-web` stops it.

### A24 · Debug a broken script

Save this intentionally broken file as scripts/broken.sh. Run it from ~/linux-lab so stray practice files stay in the lab.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.

# Set a path with a space.
folder="$HOME/linux-lab/my notes"

# BUG: unquoted expansion splits the path into two arguments.
mkdir -p $folder

# Write to note.txt, then attempt to read a different filename.
echo Practice > "$folder/note.txt"
cat "$folder/notes.txt"
```

**Assignment and check.** bash -n scripts/broken.sh checks syntax. bash -x scripts/broken.sh runs it and traces expanded commands. Fix the quoting and filename, and stop if directory creation fails. Expect Practice.

### A25 · Check integrity

Create a baseline and detect a change.

```bash
# Save a SHA-256 digest plus filename, then verify against it.
sha256sum notes/topics.txt > data/topics.sha256
sha256sum -c data/topics.sha256

# Append a line and verify again.
echo 'New topic' >> notes/topics.txt
sha256sum -c data/topics.sha256
```

**Assignment and check.** Expect OK, then FAILED. Explain why someone able to replace both the file and the checksum could make verification pass.

## B · Permissions, SSH and file transfers

### B1 · Ownership and modes

Create a permissions workspace.

```bash
# Create and enter the directory, write a file, and show your IDs and the file's metadata.
mkdir -p ~/linux-lab/permissions
cd ~/linux-lab/permissions
echo Practice > report.txt
id
ls -l report.txt
stat report.txt

# Set owner-only read/write, then owner read/write plus group read. The symbolic form has the same effect as 640.
chmod 600 report.txt
chmod 640 report.txt
chmod u=rw,g=r,o= report.txt
```

**Assignment and check.** Explain owner, group and other. Explain why granting everyone write permission with 777 exposes files to unnecessary modification.

### B2 · Directory permissions

A directory's read bit lists names, execute bit allows traversal, and write plus execute normally allows creating or removing entries.

```bash
# Make a directory with one file, then leave only owner read permission on the directory.
mkdir -p locked
echo Hello > locked/message.txt
chmod 400 locked

# Listing names works, but accessing the file through the directory fails for your normal user.
ls locked
cat locked/message.txt

# Restore owner read/write/traversal access.
chmod 700 locked
```

**Assignment and check.** Explain why deletion is controlled mainly by the parent directory, including the sticky-bit exception studied later.

### B3 · Default permissions

Use a subshell so umask changes end at the closing parenthesis.

```bash
# 022 masks group/other write. 077 masks all group/other permissions. Files normally start from 666, directories from 777 before applying the mask.
(
  umask 022
  touch public-default.txt
  mkdir public-directory
  umask 077
  touch private-default.txt
  mkdir private-directory
  ls -ld *default.txt *directory
)
```

**Assignment and check.** Use fresh names when repeating. Expect files 644/600 and directories 755/700. Existing files keep their old modes.

### B4 · Users, groups and sharing

Run once on the lab VM. If names exist, inspect them rather than recreating them.

```bash
# Create a group and a user with a home (-m) and Bash shell (-s).
sudo groupadd linuxlab
sudo useradd -m -s /bin/bash labmate

# Append (-a) supplementary group (-G) membership. Omitting -a would replace other supplementary groups.
sudo usermod -aG linuxlab "$USER"
sudo usermod -aG linuxlab labmate

# Create a shared directory, assign its owner/group, and set setgid plus owner/group access.
sudo mkdir -p /srv/linux-lab-shared
sudo chown root:linuxlab /srv/linux-lab-shared
sudo chmod 2770 /srv/linux-lab-shared
```

**Assignment and check.** Log out and back in. id confirms membership. touch /srv/linux-lab-shared/from-me.txt creates a file. ls -l shows its inherited group. chgrp linuxlab FILE changes only a file's group. Explain why the inherited group still needs write permission to edit.

### B5 · Access control lists

Grant one named user access.

```bash
# Install ACL utilities if absent, then create a root-owned file.
sudo apt install acl
sudo touch /srv/linux-lab-shared/acl-demo.txt
sudo chmod 600 /srv/linux-lab-shared/acl-demo.txt

# Add (-m) a user entry with read/write. Display the resulting ACL.
sudo setfacl -m u:labmate:rw /srv/linux-lab-shared/acl-demo.txt
getfacl /srv/linux-lab-shared/acl-demo.txt

# Run a shell as labmate so that the redirection itself uses that user's permissions.
sudo -u labmate sh -c 'echo Practice >> /srv/linux-lab-shared/acl-demo.txt'

# Remove (-x) that named user entry.
sudo setfacl -x u:labmate /srv/linux-lab-shared/acl-demo.txt
```

**Assignment and check.** Repeat the write and expect failure. Explain how the ACL mask limits named-user and group-class permissions.

### B6 · Establish SSH

On a second VM you own, use an existing normal account with a password. SERVER_IP and labuser below are placeholders. For one-VM practice use your own username and 127.0.0.1, and remember local and remote files then share one machine.

```bash
# SERVER: refresh package lists, install the SSH server, start it, and show addresses.
sudo apt update
sudo apt install openssh-server
sudo systemctl start ssh
ip -br address

# SERVER console: print the Ed25519 host key's SHA-256 fingerprint.
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub

# CLIENT: require that host-key type on first connection so you can compare the displayed fingerprint with the console.
ssh -o HostKeyAlgorithms=ssh-ed25519 labuser@SERVER_IP
```

**Assignment and check.** Accept the first host key only after matching it. whoami and hostname identify the remote session. exit leaves it. ~/.ssh/known_hosts remembers trusted host keys. Keep a VM console available.

### B7 · Generate authentication keys

Run on the client. Choose a new filename if it exists already.

```bash
# Generate an Ed25519 key pair (-t), choose its pathname (-f), and attach a label (-C). Enter a passphrase when prompted.
ssh-keygen -t ed25519 -f ~/.ssh/linux_lab_ed25519 -C linux-lab

# Copy the PUBLIC key to the remote authorized_keys using existing account access.
ssh-copy-id -i ~/.ssh/linux_lab_ed25519.pub labuser@SERVER_IP

# Choose the matching PRIVATE key for authentication.
ssh -i ~/.ssh/linux_lab_ed25519 labuser@SERVER_IP
```

**Assignment and check.** The private file stays secret on the client. The .pub file authorizes it on the server. Explain key passphrase versus account password, and user keys versus server host keys.

### B8 · Key permissions and agents

Run the first block on the client.

```bash
# Protect the SSH directory and private key. Public keys can be readable by others.
chmod 700 ~/.ssh
chmod 600 ~/.ssh/linux_lab_ed25519
chmod 644 ~/.ssh/linux_lab_ed25519.pub

# Start an agent and import its environment into this shell. Load the key, list fingerprints, then remove just that key.
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/linux_lab_ed25519
ssh-add -l
ssh-add -d ~/.ssh/linux_lab_ed25519

# Request verbose authentication diagnostics.
ssh -v -i ~/.ssh/linux_lab_ed25519 labuser@SERVER_IP
```

**Assignment and check.** On the server account run chmod 700 ~/.ssh and chmod 600 ~/.ssh/authorized_keys to restrict access. Check ownership with ls -ld. Distinguish wrong username, wrong key, permissions and connection errors.

### B9 · SSH shortcuts

Append the following configuration using nano ~/.ssh/config. Host names the shortcut, HostName supplies its address, User selects the account, IdentityFile selects the key, and IdentitiesOnly limits identities offered.

**Assignment and check.** Replace the placeholders.

```sshconfig
Host linux-lab-server
    HostName SERVER_IP
    User labuser
    IdentityFile ~/.ssh/linux_lab_ed25519
    IdentitiesOnly yes
```

```bash
# Restrict your configuration to its owner.
chmod 600 ~/.ssh/config
# Connect using the shortcut.
ssh linux-lab-server
# Run hostname remotely and return automatically when it finishes.
ssh linux-lab-server hostname
```

### B10 · SCP upload and download

Use the configured shortcut.

```bash
# Create local content and the remote destination. Quotes send the remote command as one argument.
echo 'Transfer practice' > ~/linux-lab/notes/transfer.txt
ssh linux-lab-server 'mkdir -p ~/transfer-lab'

# Copy local source to remote destination. The colon separates host and path.
scp ~/linux-lab/notes/transfer.txt linux-lab-server:~/transfer-lab/

# Copy the remote source to a different local filename.
scp linux-lab-server:~/transfer-lab/transfer.txt ~/linux-lab/notes/downloaded.txt

# Copy a whole directory recursively.
scp -r ~/linux-lab/notes linux-lab-server:~/transfer-lab/

# Compare original and downloaded contents.
diff ~/linux-lab/notes/transfer.txt ~/linux-lab/notes/downloaded.txt
```

**Assignment and check.** Expect no differences. Explain the source/destination order and -r.

### B11 · SFTP sessions

sftp linux-lab-server opens the interactive file-transfer client. Enter these at its prompt, one at a time.

**Assignment and check.** pwd shows the remote directory. lpwd shows the local one. ls lists remote names, lls lists local names. cd transfer-lab changes the remote directory. put /etc/hosts hosts-copy uploads a local file under a remote name. get hosts-copy /tmp/linux-lab-hosts-copy downloads it. mkdir practice makes a remote directory. bye closes the session. Upload a lab note and download it under a new name.

### B12 · Synchronize with rsync

Install rsync on both machines if needed using sudo apt install rsync.

```bash
# Preview changes only. -a recursively preserves common metadata where permissions allow; -v prints activity.
rsync -av --dry-run ~/linux-lab/notes/ linux-lab-server:~/transfer-lab/notes-sync/

# Apply the same synchronization.
rsync -av ~/linux-lab/notes/ linux-lab-server:~/transfer-lab/notes-sync/

# Preview destination deletions for files absent from the source. Keep this confined to this lab destination.
rsync -av --dry-run --delete ~/linux-lab/notes/ linux-lab-server:~/transfer-lab/notes-sync/
```

**Assignment and check.** Modify one note and repeat. The source's trailing slash copies its contents; omitting it includes the directory itself. Explain why a mirror can propagate accidental deletions.

### B13 · Verify transfer integrity

Compare digests on both machines.

```bash
# Hash the local file, then execute hashing on the remote copy.
sha256sum ~/linux-lab/notes/transfer.txt
ssh linux-lab-server 'sha256sum ~/transfer-lab/transfer.txt'
```

**Assignment and check.** The digest fields should match. Change the remote file and compare again.

### B14 · Forward a port

SERVER: run A21's loopback web server on port 8000. Keep that terminal open.

```bash
# CLIENT: create a local forward. -N runs no remote command. The destination 127.0.0.1:8000 is reached from the server side.
ssh -N -L 9000:127.0.0.1:8000 linux-lab-server

# A second CLIENT terminal requests the forwarded service.
curl http://127.0.0.1:9000/
```

**Assignment and check.** Stop the tunnel with Ctrl+C and repeat the request. Explain local port 9000, remote port 8000, and each machine's loopback address.

### B15 · Revoke a key

Keep an existing server session or console open.

```bash
# SERVER account: back up authorized keys, then edit the file and remove only the linux-lab public-key line.
cp -p ~/.ssh/authorized_keys ~/.ssh/authorized_keys.lab-backup
nano ~/.ssh/authorized_keys

# CLIENT: permit only public-key authentication and select the lab key via the shortcut.
ssh -o PreferredAuthentications=publickey -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no linux-lab-server
```

**Assignment and check.** If other authorized identities exist, remove them from this test's authentication selection before drawing a conclusion. Expect failure for the revoked lab key. Restore the saved file with cp -p from the open server session. Explain why existing sessions remain connected.

## C · Bash and Python scripting

Save each full script using nano in ~/linux-lab/scripts. Run it with bash PATH or python3 PATH. Comments explain the line or block immediately below. Later exercises ask you to assemble commands already introduced.

### C1 · System introduction

Expand A16.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.

# printf substitutes values into %s. $(...) captures another command's output.
printf 'User: %s\nHost: %s\nDirectory: %s\nDate: %s\n' "$USER" "$(hostname)" "$PWD" "$(date)"
```

**Assignment and check.** Save as hello-system.sh, run it, then add uname -r output.

### C2 · Read input

Save as greet.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.

# Read a full line without processing backslashes; -p displays a prompt.
read -r -p 'Your name? ' name

# -z tests for an empty string. >&2 directs the message to errors.
if [[ -z "$name" ]]; then
  printf 'A name is required.\n' >&2
  exit 1
fi

# Print the supplied name without interpreting it as a format string.
printf 'Welcome, %s!\n' "$name"
```

**Assignment and check.** Test empty input and a name with spaces. Add a directory prompt and -d test.

### C3 · Arguments

Expand A17 into inspect.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.
if [[ $# -ne 1 ]]; then
  printf 'Usage: %s PATH\n' "$0" >&2
  exit 2
fi

# Test a symlink before its target type. -L checks link, -f regular file, -d directory.
if [[ -L "$1" ]]; then
  echo 'Symbolic link'
elif [[ -f "$1" ]]; then
  echo 'Regular file'
elif [[ -d "$1" ]]; then
  echo 'Directory'
else
  echo 'Other type or missing path' >&2
  exit 1
fi
```

**Assignment and check.** Test file, directory, missing path, and symlink. Explain why -L is checked first.

### C4 · Access checks

Write check-access.sh PATH after validating one argument.

```bash
# Each test reports access for the calling user. && runs the print only if the test succeeds.
[[ -r "$1" ]] && echo readable
[[ -w "$1" ]] && echo writable
[[ -x "$1" ]] && echo executable
```

**Assignment and check.** Use explicit if/else blocks to also report denied access and return a deliberate status. Test a lab file at 600, 400 and 700 as your normal user.

### C5 · Loops

Write create-files.sh COUNT.

```bash
# Accept only 1–100. =~ applies a regular expression; || succeeds if either condition is true.
if [[ $# -ne 1 ]] || [[ ! "$1" =~ ^([1-9][0-9]?|100)$ ]]; then
  echo 'Supply a count from 1 to 100.' >&2
  exit 2
fi

# Create the destination, then use arithmetic loop initialization, condition and increment.
destination="$HOME/linux-lab/data/loop-practice"
mkdir -p "$destination" || exit 1
for ((number=1; number<=$1; number++)); do
  printf 'Practice file %s\n' "$number" > "$destination/file-$number.txt" || exit 1
done
```

**Assignment and check.** Add the Bash shebang. Reject zero, negative, empty and nonnumeric input before creating anything. Explain || exit 1.

### C6 · Functions and menus

Build menu.sh from these functions.

```bash
# Define named blocks. They execute when called.
show_date() { date; }
show_disk() { df -h "$HOME"; }
show_memory() { free -h; }

# Repeat while true succeeds. case dispatches by input; ;; ends each branch. EOF exits through read's failure.
while true; do
  printf '1 Date\n2 Disk\n3 Memory\n4 Exit\n'
  read -r choice || break
  case "$choice" in
    1) show_date ;;
    2) show_disk ;;
    3) show_memory ;;
    4) break ;;
    *) echo 'Choose 1–4.' ;;
  esac
done
```

**Assignment and check.** Add the shebang. Confirm invalid choices and end-of-input behave sensibly.

### C7 · Safe filename processing

Extend A18 into list-text-files.sh DIRECTORY.

```bash
# Use the argument or fall back to notes. Reject a non-directory.
directory="${1:-$HOME/linux-lab/notes}"
if [[ ! -d "$directory" ]]; then
  echo 'Directory missing' >&2
  exit 1
fi

# Initialize the counter; ((...)) performs arithmetic. NUL delimiters handle spaces and newlines in filenames.
count=0
while IFS= read -r -d '' file; do
  printf '%s: ' "$file"
  wc -l < "$file"
  count=$((count + 1))
done < <(find "$directory" -type f -name '*.txt' -print0)
printf 'Files: %s\n' "$count"
```

**Assignment and check.** Add the shebang. Test spaces and literal * in filenames. Investigate how to detect find failures as an advanced extension.

### C8 · Log analyzer

Create the fixture, then write analyze-log.sh FILE.

```bash
# Write five log messages to a fixture.
printf '%s\n' 'INFO Service started' 'ERROR Connection failed' 'INFO Retrying' 'WARNING Slow response' 'ERROR Request failed' > ~/linux-lab/data/application.log

# Count matching lines. grep returns 1 when none match, even though this can be a valid result.
grep -c '^ERROR ' ~/linux-lab/data/application.log

# Write only error lines to a report.
grep '^ERROR ' ~/linux-lab/data/application.log > ~/linux-lab/reports/errors.txt
```

**Assignment and check.** Validate an argument and readability (-r). Count INFO, WARNING, ERROR. Expect 2/1/2. Handle grep status 1 as no matches and status 2 as an error. Test a log with zero errors.

### C9 · Logging and error handling

Use this pattern inside a script after validating source and destination arguments.

```bash
# A function prefixes its arguments ($*) with a timestamp and writes to standard error.
log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" >&2
}

# if tests cp's status directly. Save $? immediately in the failure branch before another command changes it.
if cp -- "$source" "$destination"; then
  log 'Copy completed'
else
  status=$?
  log "Copy failed with status $status"
  exit "$status"
fi
```

**Assignment and check.** Set source=$1 and destination=$2 after requiring two arguments. Test a missing source and an unwritable destination. set -u treats unset expansion as an error. set -o pipefail lets pipeline failures affect its status. Study help set before using set -e, whose conditional exceptions require care.

### C10 · Backup tool

Write backup.sh SOURCE DESTINATION using A10 and C9.

```bash
# Resolve existing source path and normalize a destination that may not exist. -e requires all components to exist; -m permits missing components.
realpath -e -- "$source"
realpath -m -- "$destination"
```

**Assignment and check.** Validate both arguments, create the destination, reject equal/nested destination paths, prevent archive overwrites, log failures and create a checksum. Test a path containing spaces and restore nested/empty directories. These are design hints, not a full solution.

### C11 · Automated transfer

Write send-backup.sh ARCHIVE SSH_HOST REMOTE_DIRECTORY.

```bash
# Fail rather than waiting for interactive authentication. A loaded agent or other working noninteractive key access is needed.
ssh -o BatchMode=yes linux-lab-server true

# Copy an archive using key authentication, failing if interaction would be required.
scp -o BatchMode=yes "$archive" "$ssh_host:$remote_directory/"
```

**Assignment and check.** Require three arguments, a readable archive and a restricted lab remote path using only letters, digits, slash, dot, underscore and hyphen. Reject parent components. Avoid constructing remote shell text from unchecked input. Use B13 to verify remotely, log outcomes, and test unavailable server and invalid path.

### C12 · Permissions auditor

Write audit-permissions.sh DIRECTORY.

```bash
# Find regular files with the world-write bit set, then directories with that bit.
find "$directory" -type f -perm -0002 -print
find "$directory" -type d -perm -0002 -print

# Display numeric permission and owner metadata for a designated private lab key.
stat -c '%a %U %n' ~/.ssh/linux_lab_ed25519
```

**Assignment and check.** Validate the directory. Report findings and traversal failures. Check only designated private key files for excessive permissions. An optional explicit repair flag may apply chmod 600 to those files. Default execution must report only.

### C13 · Parse options

Build --source, --destination, --dry-run, --verbose and --help.

```bash
# shift consumes processed arguments. ${2:-} avoids an unset expansion for a missing value.
while [[ $# -gt 0 ]]; do
  case "$1" in
    --source)
      [[ $# -ge 2 && -n "${2:-}" ]] || { echo 'Missing source' >&2; exit 2; }
      source=$2
      shift 2
      ;;
    --dry-run) dry_run=true; shift ;;
    --help) echo 'Usage: tool --source DIR [--dry-run]'; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
done
```

**Assignment and check.** Initialize variables before parsing and add remaining options. Reject missing required values before work. A dry-run prints intended actions. Test unknown options and paths with spaces.

### C14 · Temporary files and traps

Save as temporary.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.
temporary_directory=$(mktemp -d) || exit 1

# Register cleanup for shell exit. INT and TERM handlers exit with conventional signal-derived statuses.
cleanup() { rm -rf -- "$temporary_directory"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# Write only inside the generated directory and pause for the interruption test.
printf '%s\n' "$temporary_directory"
echo Practice > "$temporary_directory/data.txt"
sleep 30
```

**Assignment and check.** Run normally and with Ctrl+C, confirming removal. rm -rf recursively removes the exact quoted temporary directory. Keep its value fixed after creation. Explain why SIGKILL and power failure cannot trigger cleanup.

### C15 · Prevent concurrent runs

Save as lock-demo.sh.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.
mkdir -p "$HOME/linux-lab/run" || exit 1
exec 9>"$HOME/linux-lab/run/backup.lock"
if ! flock -n 9; then
  echo 'Another instance is running.' >&2
  exit 1
fi

# Keep the process and lock alive for 20 seconds.
echo Working
sleep 20
```

**Assignment and check.** Launch two copies in separate terminals. Only one proceeds. Explain why the lock is released when its held file descriptor closes.

### C16 · Retry with limits

Run against A21's server.

```bash
#!/usr/bin/env bash
# The shebang selects Bash when executing this saved file directly.
for attempt in {1..5}; do
  if curl -fsS --max-time 2 http://127.0.0.1:8000/; then
    exit 0
  fi
  if [[ "$attempt" -lt 5 ]]; then
    sleep "$attempt"
  fi
done
exit 1
```

**Assignment and check.** Start before the server, then start the server during retries. Repeat with no server. Expect success and failure respectively.

### C17 · Review and debug

Apply checks to your backup script.

```bash
# Check syntax without executing, then execute with expanded-command tracing.
bash -n ~/linux-lab/scripts/backup.sh
bash -x ~/linux-lab/scripts/backup.sh

# If installed, statically analyze the script for common mistakes.
shellcheck ~/linux-lab/scripts/backup.sh
```

**Assignment and check.** Install ShellCheck if needed using sudo apt install shellcheck. Supply required backup arguments when tracing. Test missing source, unwritable destination, spaces, nested destination and repeated runs. Traces can reveal secrets, so use lab data.

### C18 · Python file inventory

Write inventory.py using the standard library.

**Assignment and check.** Use argparse.ArgumentParser to define directory and output arguments. pathlib.Path.rglob('*') walks the directory tree, Path.is_symlink identifies links, Path.stat reads metadata, and json.dump serializes your records to a file. Catch OSError per item and record inaccessible entries. Define your link policy, exclude the output from its own inventory, and return nonzero on incomplete scanning.

```bash
# Run your Python program with its input directory and output option.
python3 ~/linux-lab/scripts/inventory.py ~/linux-lab/notes --output ~/linux-lab/reports/inventory.json
```
Record relative paths and sizes, plus SHA-256 content digests if you want reliable changed-content detection. Compare two inventories for additions, removals and modifications.

### C19 · Python subprocesses

Save a Python script around this example. Each list element is one argument. capture_output collects stdout/stderr, text returns strings, check raises on failure, timeout bounds runtime.

**Assignment and check.**

```python
import subprocess

try:
    result = subprocess.run(
        ['df', '-h'], capture_output=True, text=True,
        check=True, timeout=10,
    )
    print(result.stdout, end='')
except FileNotFoundError:
    raise SystemExit('Command is missing')
except subprocess.TimeoutExpired:
    raise SystemExit('Command timed out')
except subprocess.CalledProcessError as error:
    print(error.stderr, end='')
    raise SystemExit(error.returncode)
```
import loads a module. try/except dispatches failures by exception type. SystemExit ends the program with failure when given a message. print end='' avoids an extra newline. Run with python3, save a report using Python's open, and test a missing command.

## D · Extension labs

### D1 · Hard and symbolic links

Work in ~/linux-lab/permissions.

```bash
# Write content, create a second hard-link name, and create a symbolic link containing the original pathname.
echo Content > original.txt
ln original.txt hard.txt
ln -s original.txt symbolic.txt

# Show inode numbers (-i) and details, remove the original name, then read through each link.
ls -li original.txt hard.txt symbolic.txt
rm original.txt
cat hard.txt
cat symbolic.txt
```

**Assignment and check.** The hard link still reaches the inode; the symlink's pathname now has no target. Explain hard-link filesystem boundaries.

### D2 · Sticky bit

Inspect shared temporary storage.

```bash
# Show the directory entry itself (-d), including its mode.
ls -ld /tmp
```

**Assignment and check.** Find the t in its mode. Explain how a sticky directory restricts removal/renaming to the entry owner, directory owner or privileged process. Contrast with plain group-writable sharing in B4.

### D3 · Sudo rules

Inspect your effective administrative authorization.

```bash
# List commands your account may run through sudo.
sudo -l

# Print the effective username under an authorized elevated execution.
sudo whoami
```

**Assignment and check.** Explain the password prompt, effective user, and why a permission test under sudo can differ from the same test as your normal user.

### D4 · Filesystems and mounting

Use a new 64 MiB image file, which avoids selecting a real disk. Run from ~/linux-lab. Install e2fsprogs if mkfs.ext4 is absent. Use a fresh filename if this lab was already run.

```bash
# Refuse an existing image and allocate a sparse regular file.
test ! -e data/disk-lab.img && truncate -s 64M data/disk-lab.img

# Create an ext4 filesystem inside that lab image. Formatting replaces its previous contents.
mkfs.ext4 data/disk-lab.img

# Create a mountpoint, then attach the image through a loop device.
sudo mkdir -p /mnt/linux-lab-image
sudo mount -o loop "$HOME/linux-lab/data/disk-lab.img" /mnt/linux-lab-image

# Give your normal user ownership of the filesystem root so you can write there.
sudo chown "$USER:$(id -gn)" /mnt/linux-lab-image

# Create a file, inspect the mount, then unmount it.
echo Persist > /mnt/linux-lab-image/test.txt
findmnt /mnt/linux-lab-image
sudo umount /mnt/linux-lab-image
```

**Assignment and check.** Execute the formatting step only after the creation check succeeds. Mount again and verify test.txt persists. Explain loop device, filesystem, mountpoint, and ownership.

### D5 · Persistent mount configuration

Use a second, disposable virtual disk attached to the VM and a VM snapshot. Identify it by size/serial in lsblk output before any formatting. Use the VM console for this lab. DEVICE below is a placeholder, never paste it as a literal device name.

```bash
# Display devices, filesystem labels and UUIDs.
lsblk -f

# Read the verified lab filesystem's UUID. -s selects the field; -o value prints only its value.
sudo blkid -s UUID -o value DEVICE

# Back up the mount table configuration and edit it with the privileged editor workflow.
sudo cp -p /etc/fstab /etc/fstab.linux-lab-backup
sudoedit /etc/fstab

# Check table syntax/usability and reload systemd's generated units.
sudo findmnt --verify --verbose
sudo systemctl daemon-reload
```

**Assignment and check.** Create an ext4 filesystem on the verified disposable disk using mkfs.ext4 DEVICE, then create /mnt/linux-lab-disk with sudo mkdir -p. Add `UUID=YOUR_UUID /mnt/linux-lab-disk ext4 defaults,nofail 0 2` to fstab. UUID selects the filesystem, ext4 names its type, defaults selects standard options, nofail permits boot without it, 0 disables dump scheduling, and 2 requests a later filesystem check. Use sudo mount /mnt/linux-lab-disk to test this entry. Verify using findmnt and a test file before rebooting. Explain which effects nofail has when the disk is absent.

### D6 · Diagnose the network in layers

Use only your lab machines.

```bash
# Check interface configuration, gateway routing, hostname resolution, then TCP listeners.
ip -br address
ip route
getent hosts linux-lab-server
ss -ltn

# Try SSH with a five-second connection timeout and verbose diagnostics.
ssh -v -o ConnectTimeout=5 linux-lab-server
```

**Assignment and check.** An SSH Host shortcut is resolved by SSH config and may fail getent. Try the actual server hostname there instead. Distinguish DNS failure, no route, refused connection, timeout and denied authentication.

### D7 · Firewall rule experiment

Use the server console and a snapshot. This exercise uses a separate nftables table affecting only a temporary web port. Install nftables if absent. Use the server's private address for SERVER_IP and client address for CLIENT_IP.

```bash
# SERVER: expose the lab page on its interfaces for this private-network experiment.
python3 -m http.server 8081 --bind 0.0.0.0 --directory ~/linux-lab/web

# Another SERVER terminal: create an isolated rule table and an input chain. The quoted definition preserves nft syntax.
sudo nft add table inet linuxlab
sudo nft 'add chain inet linuxlab input { type filter hook input priority 0; policy accept; }'

# Allow your client to this port, then drop other TCP connections to the same port. Replace CLIENT_IP before execution.
sudo nft add rule inet linuxlab input ip saddr CLIENT_IP tcp dport 8081 accept
sudo nft add rule inet linuxlab input tcp dport 8081 drop

# Inspect your rules, then remove only the lab table after testing.
sudo nft list table inet linuxlab
# Run after client tests.
sudo nft delete table inet linuxlab
```

**Assignment and check.** From the client, curl --max-time 3 http://SERVER_IP:8081/ bounds the request to three seconds. Test with the allow rule, then without it by recreating this lab table with only the drop rule. Existing firewall rules can also affect results. Stop the web server and remove the table. Explain rule order. Verify SSH continues to work.

### D8 · Rotate a practice log

Run from ~/linux-lab.

```bash
# Create a log with restrictive directory access and open a user-owned configuration.
mkdir -p logs
chmod 700 logs
echo 'Application started' > logs/app.log
nano logrotate-lab.conf
```

**Assignment and check.** Write this configuration, replacing /home/YOU with your actual home path.

```text
/home/YOU/linux-lab/logs/app.log {
    size 1k
    rotate 3
    compress
    missingok
    notifempty
    create 0600
}
```
size triggers at 1 KiB, rotate retains three generations, compress gzips older logs, missingok tolerates absence, notifempty skips empty files, and create makes a fresh owner-only log.

```bash
# Preview with a dedicated state file. -d makes no changes.
logrotate -d -s "$HOME/linux-lab/run/logrotate.state" "$HOME/linux-lab/logrotate-lab.conf"
# Force a rotation (-f), using your own state file rather than system state.
logrotate -f -s "$HOME/linux-lab/run/logrotate.state" "$HOME/linux-lab/logrotate-lab.conf"
```
Inspect logs with ls -l. Append a message and repeat. Explain how applications holding open log descriptors need reopen coordination.

### D9 · Systemd backup timer

Use your working A19 backup script. Create these files under ~/.config/systemd/user.

**Assignment and check.** **lab-backup.service file contents**

```ini
[Unit]
Description=Back up Linux lab notes
[Service]
Type=oneshot
ExecStart=/usr/bin/bash %h/linux-lab/scripts/backup-notes.sh
```
Type=oneshot waits for the command to finish. ExecStart runs your script with Bash.

**lab-backup.timer file contents**

```ini
[Unit]
Description=Daily Linux lab backup
[Timer]
OnCalendar=daily
Persistent=true
[Install]
WantedBy=timers.target
```
OnCalendar schedules midnight in the VM's time zone. Persistent catches a missed scheduled run when the timer becomes active. User timers depend on the user manager running.

```bash
# Reload definitions, enable startup and activate this timer now.
systemctl --user daemon-reload
systemctl --user enable --now lab-backup.timer
# Inspect schedule, execute the backup once now, and inspect its logs.
systemctl --user list-timers
systemctl --user start lab-backup.service
journalctl --user -u lab-backup.service -n 20 --no-pager
# Disable automatic runs after the exercise.
systemctl --user disable --now lab-backup.timer
```
Verify an archive was created and restore it.

### D10 · Version scripts with Git

Use only your lab scripts in this repository.

```bash
# Initialize repository metadata in scripts and set a local practice identity.
cd ~/linux-lab/scripts
git init
git config user.name 'Linux Student'
git config user.email 'student@example.invalid'

# Stage one script, commit it, then create and switch to a branch.
git add hello-system.sh
git commit -m 'Add system greeting'
git switch -c improve-greeting

# Inspect changes, current status and short history.
git diff
git status
git log --oneline

# After saving any wanted edits, discard unstaged changes only to this tracked practice file.
git restore hello-system.sh
```

**Assignment and check.** Modify the greeting, inspect the diff and commit it. Make another disposable edit and restore it. Explain working directory, staging area, commit and branch.

### D11 · Resource limits

A temporary Bash process contains the modified limit.

```bash
# Print the open-descriptor soft limit, set it to 64, then print it again.
bash -c 'ulimit -Sn; ulimit -Sn 64; ulimit -Sn'

# Print the hard ceiling for the current shell.
ulimit -Hn
```

**Assignment and check.** Write a Python program that opens /dev/null repeatedly, keeps each handle in a list, catches OSError, and closes all handles in finally. Run it with `bash -c 'ulimit -Sn 64; python3 ~/linux-lab/scripts/open-files.py'`. -c executes the quoted script, ulimit limits that shell and its child, and python3 runs the program. Compare with a bounded test under the original limit. Explain why standard streams also occupy descriptors.

## E · Integrated projects and marking guide

These consolidate every earlier capstone. Use the command explanations in A–D when choosing your implementation. Keep an execution log with the exact command, expected result, actual result and any fix.

### E1 · System health report

Write health-report.sh. Report date, hostname, uptime, memory, disk usage, the five processes using most memory, failed system services and listening TCP ports.

```bash
# uptime prints time running and system load.
uptime
# Order processes by descending resident memory and select five data rows plus the header.
ps -eo pid,comm,rss --sort=-rss | head -n 6
```

Use A12, A14 and A15 for the other checks. Save a timestamped report under reports. Run as your normal user, mark inaccessible information clearly, and return failure when a required check cannot run. Distinguish “no failed services” from failure to perform the check.

### E2 · Local backup and recovery

Extend C10 with checksums and a restore command. Require an existing source and a separate destination, reject a destination inside the source, and avoid overwriting old archives. Verify the checksum before extracting only archives made for this lab. Restore to a newly created empty directory and compare against a saved original fixture.

Pass when files with spaces, nested directories and empty directories are recovered, while an intentionally corrupted archive is rejected. Include logs of both outcomes.

### E3 · Service incident investigation

Use A21–A23 to create five failures, one at a time. Occupy the listening port, choose the wrong document directory, request a missing page, put an invalid executable in ExecStart, and stop the service.

For each incident, record symptom, exact diagnostic commands, evidence, root cause, fix and successful verification. Restore the unit configuration between tests. Pass when you can explain each failure without rebooting.

### E4 · Secure remote backup

Combine A19, B7–B15, C10–C17 and D9 into one workflow. Accept source, destination host and a dedicated remote directory. Use a passphrase-protected key with an agent, protected local files and remote directories, timestamped archives, integrity verification, logs, deliberate exit codes, dry-run, a lock, cleanup and bounded retries. Schedule it using either cron or a user timer.

Pass when you transfer a backup to the second VM, remove only a disposable source copy, restore into a fresh directory and prove content equality. Demonstrate rejecting a corrupted copy and revoking the backup key. On a one-VM setup, this demonstrates the mechanics; repeat on a second VM to verify recovery across machines.

## Progress record

For every lab record:

- The exercise ID and completion date.
- The command you ran and what each option means.
- One successful check and one failure you investigated.
- Any remaining question.

Complete the course when you can repeat the projects from your own notes, explain each command you chose and recover from the deliberate failures.

