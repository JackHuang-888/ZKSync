# Zookeeper Data Synchronization Tool (ZKSync)

**ZKSync** is a tool designed to synchronize Zookeeper data to another Zookeeper server. It supports syncing both
non-ephemeral and ephemeral nodes (optional). This tool offers flexible configuration options, including authentication,
node exclusion, and logging.

## Installation

Before running ZKSync, make sure you have the following dependencies installed:

- Python 3.x
- Kazoo: You can install it using the following pip command:

```bash
pip install -r requirements.txt
```

## Usage

When running ZKSync, you can configure it using the following command-line parameters:

```bash
python zksync.py --source-server SOURCE_SERVER --target-server TARGET_SERVER --source-root SOURCE_ROOT --target-root TARGET_ROOT [--sync-ephemeral-nodes] [--source-auth SOURCE_AUTH [SOURCE_AUTH ...]] [--target-auth TARGET_AUTH [TARGET_AUTH ...]] [--ignore-nodes IGNORE_NODES [IGNORE_NODES ...]] [--log-file LOG_FILE] [--log-max-size LOG_MAX_SIZE] [--log-backup-count LOG_BACKUP_COUNT]
```

### Parameter Description

- --source-server SOURCE_SERVER: Specify the address (host:port) of the source Zookeeper server.
- --target-server TARGET_SERVER: Specify the address (host:port) of the target Zookeeper server.
- --source-root SOURCE_ROOT: Specify the source root node.
- --target-root TARGET_ROOT: Specify the target root node.
- --sync-ephemeral-nodes: (Optional) Sync ephemeral nodes. If not specified, ephemeral nodes won't be synchronized.
- --source-auth SOURCE_AUTH [SOURCE_AUTH ...]: (Optional) Specify authentication information for the source server in
  the format 'schema:credential'. Multiple authentication information can be provided.
- --target-auth TARGET_AUTH [TARGET_AUTH ...]: (Optional) Specify authentication information for the target server in
  the format 'schema:credential'. Multiple authentication information can be provided.
- --ignore-nodes IGNORE_NODES [IGNORE_NODES ...]: (Optional) Specify a list of nodes to ignore during the
  synchronization process.
- --log-file LOG_FILE: (Optional) Specify the path to the log file. Default is sync_zookeeper.log.
- --log-max-size LOG_MAX_SIZE: (Optional) Specify the maximum size of the log file in bytes. Default is 10MB.
- --log-backup-count LOG_BACKUP_COUNT: (Optional) Specify the number of old log file backups to retain. Default is 5.

## Example

Here is an example usage:

```bash
python zksync.py --source-server localhost:2181 --target-server remotehost:2181 --source-root /source --target-root /target --sync-ephemeral-nodes --source-auth digest:user:password --ignore-nodes /source/temp_node --log-file zksync.log --log-max-size 20971520 --log-backup-count 3
```

This example syncs data from the local Zookeeper server's /source node to the remote Zookeeper server's /target node,
syncing ephemeral nodes as well and using authentication information digest:user:password for the connection. It ignores
the /source/temp_node during the synchronization process. Logs are recorded in the zksync.log file with a maximum size
of 20MB and 3 old log file backups.

## Notes

- Make sure you have correctly installed the Kazoo dependency.
- Exercise caution when using authentication to protect your credentials.
- Log files can be configured according to your needs for better tracking of the synchronization process and issues.