# Paper MC systemd scripts

Steps for using the provided scripts and setting up the __Paper MC__ server as a __systemd__ service.  This will allow you to control the server with `systemctl` and interact with it using the `minecraft` command.

-----

## Create Service Account

Create a user account named `minecraft`.  This will be the service account for running the server.
```
sudo useradd -m -r minecraft
sudo passwd minecraft
```

## Download Paper MC

Log into the minecraft service account.  Download __Paper__ server from:
<https://papermc.io/software/paper>

Place the server in `/home/minecraft/paper` then rename the __Paper__ server executable file to `server.jar`.

Using the commands below, replacing for the correct download URL and filename:
```
mkdir paper
cd paper
wget https://api.papermc.io/v2/projects/paper/GETLATESTFROMWEBSITE
mv paper-x.xx.x-xxx.jar server.jar
```

*Note:* If this is the first time you're running __Paper__ on your server, you'll want to manually run it at this point to agree to its EULA.

Run:
```
java -Xms4G -Xmx4G -jar server.jar --nogui
```
And follow the on screen prompts.

## Configure scripts

Switch back to your primary account with __sudo__ access.

Clone this repo:
```
git clone https://github.com/AtomicSponge/paper-systemd.git
cd paper-systemd
```

Place the file `minecraft` in `/usr/local/bin` and make sure it has execute permissions by running:
```
sudo chmod +x minecraft
sudo mv minecraft /usr/local/bin
```

Place files `minecraft.service` and `minecraft.socket` in `/etc/systemd/system`:
```
sudo mv minecraft.service /etc/systemd/system
sudo mv minecraft.socket /etc/systemd/system
```

Then to start the service run:
```
sudo systemctl enable minecraft
```

## Memory Setting

Default memory setting is 4GB, to change edit `minecraft.service` and update the following under `ExecStart` to your desired values:
```
-Xms4096M -Xmx4096M
```

## Usage

Commands are passed to the server via the provided script.

To run commands, enter the server command after `minecraft`:
```
minecraft kick PlayerName
```

<sub>*Note:* Do not use / before the command name</sub>

To view server output use the `journalctl` commmand.

For example, this will list the entire log:
```
journalctl -u minecraft.service
```

-----

### References

For a list of server commands see:
<https://minecraft.fandom.com/wiki/Commands>

Service script is using the Aikar's flags from:
<https://docs.papermc.io/misc/tools/start-script-gen>

`journalctl` manual:
<https://www.man7.org/linux/man-pages/man1/journalctl.1.html>
