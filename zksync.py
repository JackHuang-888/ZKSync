import argparse
import logging
from logging.handlers import RotatingFileHandler

from kazoo.client import KazooClient
from kazoo.exceptions import AuthFailedError


def sync_zookeeper_data(source_server, target_server, source_root, target_root, sync_ephemeral_nodes, source_auth=None,
                        target_auth=None, ignore_nodes=None):
    source_client = KazooClient(hosts=source_server)
    target_client = KazooClient(hosts=target_server)
    try:
        source_client.start()
        target_client.start()
        if source_auth:
            for auth_info in source_auth:
                auth_info_list = auth_info.split(":")
                schema = auth_info_list[0]
                credential = ":".join(auth_info_list[1:])
                source_client.add_auth(schema, credential)
                target_client.add_auth(schema, credential)
        if target_auth:
            for auth_info in target_auth:
                auth_info_list = auth_info.split(":")
                schema = auth_info_list[0]
                credential = ":".join(auth_info_list[1:])
                target_client.add_auth(schema, credential)

        def sync_node(node_path):
            try:
                source_data, source_stat = source_client.get(node_path)
                target_path = node_path.replace(source_root, target_root + "/", 1)
                if node_path in ignore_nodes:
                    logging.info(f"Ignoring node: {node_path}")
                    return
                if source_stat.ephemeralOwner != 0 and not sync_ephemeral_nodes:
                    logging.info(f"Not syncing ephemeral node: {node_path}")
                    return
                if not target_client.exists(target_path):
                    create_kwargs = {'makepath': True}
                    target_client.create(target_path, **create_kwargs)
                target_client.set(target_path, source_data)
                source_children = source_client.get_children(node_path)
                for child in source_children:
                    sync_node(("" if node_path == "/" else node_path) + '/' + child)
            except Exception as e:
                logging.error(f"Error syncing node {node_path}: {e}")

        sync_node(source_root)
    except AuthFailedError:
        logging.error("Authentication failed. Check your auth credentials.")
    finally:
        source_client.stop()
        target_client.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zookeeper Data Synchronization Tool")
    parser.add_argument("--source-server", required=True, help="Source Zookeeper server (host:port)")
    parser.add_argument("--target-server", required=True, help="Target Zookeeper server (host:port)")
    parser.add_argument("--source-root", required=True, help="Source root node")
    parser.add_argument("--target-root", required=True, help="Target root node")
    parser.add_argument("--sync-ephemeral-nodes", action="store_true", help="Sync ephemeral nodes")
    parser.add_argument("--source-auth", nargs="+",
                        help="Source server authentication in the format 'schema:credential'")
    parser.add_argument("--target-auth", nargs="+",
                        help="Target server authentication in the format 'schema:credential'")
    parser.add_argument("--ignore-nodes", nargs="*", help="List of nodes to ignore during sync")
    parser.add_argument("--log-file", help="Path to the log file")
    parser.add_argument("--log-max-size", type=int, default=10 * 1024 * 1024, help="Max size of the log file in bytes")
    parser.add_argument("--log-backup-count", type=int, default=5, help="Number of backup log files to keep")

    args = parser.parse_args()
    source_server = args.source_server
    target_server = args.target_server
    source_root = args.source_root
    target_root = args.target_root
    sync_ephemeral_nodes = args.sync_ephemeral_nodes
    source_auth = args.source_auth
    target_auth = args.target_auth
    ignore_nodes = args.ignore_nodes or []
    log_file = args.log_file
    log_max_size = args.log_max_size
    log_backup_count = args.log_backup_count

    log_file = log_file if log_file else "zk_sync.log"
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    rotating_handler = RotatingFileHandler(log_file, maxBytes=log_max_size, backupCount=log_backup_count)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    rotating_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(rotating_handler)
    sync_zookeeper_data(source_server, target_server, source_root, target_root, sync_ephemeral_nodes, source_auth,
                        target_auth, ignore_nodes)
