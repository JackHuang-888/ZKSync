# Zookeeper 数据同步工具 (ZKSync)

**ZKSync** 是一个用于将Zookeeper数据同步到另一个Zookeeper服务器的工具。它支持同步非临时和临时节点（可选）。此工具提供了灵活的参数配置，包括认证、节点排除和日志选项。

## 安装

在运行 ZKSync 之前，请确保已安装以下依赖项：

- Python 3.x
- Kazoo：您可以使用以下 pip 命令安装它：

```bash
pip install -r requirements.txt
```

## 用法

运行ZKSync时，可以使用以下命令行参数进行配置：

```bash
python zksync.py --source-server SOURCE_SERVER --target-server TARGET_SERVER --source-root SOURCE_ROOT --target-root TARGET_ROOT [--sync-ephemeral-nodes] [--source-auth SOURCE_AUTH [SOURCE_AUTH ...]] [--target-auth TARGET_AUTH [TARGET_AUTH ...]] [--ignore-nodes IGNORE_NODES [IGNORE_NODES ...]] [--log-file LOG_FILE] [--log-max-size LOG_MAX_SIZE] [--log-backup-count LOG_BACKUP_COUNT]
```

### 参数说明

- --source-server SOURCE_SERVER：指定源 Zookeeper 服务器的地址（host:port）。
- --target-server TARGET_SERVER：指定目标 Zookeeper 服务器的地址（host:port）。
- --source-root SOURCE_ROOT：指定源根节点。
- --target-root TARGET_ROOT：指定目标根节点。
- --sync-ephemeral-nodes：（可选）同步临时节点，如果不指定此参数，则不同步临时节点。
- --source-auth SOURCE_AUTH [SOURCE_AUTH ...]：（可选）指定源服务器的认证信息，格式为 'schema:credential'，可支持多个认证信息。
- --target-auth TARGET_AUTH [TARGET_AUTH ...]：（可选）指定目标服务器的认证信息，格式为 'schema:credential'，可支持多个认证信息。
- --ignore-nodes IGNORE_NODES [IGNORE_NODES ...]：（可选）指定要在同步过程中忽略的节点列表。
- --log-file LOG_FILE：（可选）指定日志文件的路径，默认为 sync_zookeeper.log。
- --log-max-size LOG_MAX_SIZE：（可选）指定日志文件的最大大小（字节），默认为 10MB。
- --log-backup-count LOG_BACKUP_COUNT：（可选）指定要保留的旧日志文件数量，默认为 5。

## 示例

以下是使用示例：

```bash
python zksync.py --source-server localhost:2181 --target-server remotehost:2181 --source-root /source --target-root /target --sync-ephemeral-nodes --source-auth digest:user:password --ignore-nodes /source/temp_node --log-file zksync.log --log-max-size 20971520 --log-backup-count 3
```

此示例将从本地 Zookeeper 服务器的 /source 节点同步数据到远程 Zookeeper 服务器的 /target 节点，同时同步临时节点，并使用认证信息 digest:user:password 进行连接。忽略同步过程中的
/source/temp_node 节点。日志将记录在 zksync.log 文件中，最大大小为 20MB，并保留 3 个旧日志文件备份。

## 注意事项

- 请确保已正确安装 Kazoo 依赖项。
- 在使用认证时，请小心保护您的认证信息。
- 日志文件可以根据您的需求进行配置，以便更好地跟踪同步过程和问题。

ZKSync 是一个方便且强大的工具，可帮助您轻松管理 Zookeeper 数据的同步。如果您遇到任何问题或有任何建议，请随时与我们联系。