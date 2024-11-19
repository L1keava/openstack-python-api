import json
import yaml
from kubernetes import client, config

def main():
    # 加载 Kubernetes 配置
    config.load_kube_config()  # 加载 ~/.kube/config

    # 创建一个 AppsV1 API 实例
    apps_v1_api = client.AppsV1Api()

    # 加载 YAML 文件
    yaml_file_path = '/root/nginx-deployment.yaml'
    with open(yaml_file_path) as f:
        dep_manifest = yaml.safe_load_all(f)
        for deployment in dep_manifest:
            # 创建 Deployment
            namespace = "default"  # 根据需要修改命名空间
            apps_v1_api.create_namespaced_deployment(
                namespace=namespace,
                body=deployment
            )
            print(f"Deployment '{deployment['metadata']['name']}' created.")

    # 查询 Deployment 信息
    deployment_info = apps_v1_api.read_namespaced_deployment(
        name="nginx-deployment",
        namespace=namespace
    )

    # 输出 Deployment 信息
    print(deployment_info)

    # 将 Deployment 信息写入 JSON 文件
    with open("deployment_sdk_dev.json", "w") as json_file:
        json.dump(deployment_info.to_dict(), json_file, indent=4)

    print("Deployment information has been saved to deployment_sdk_dev.json.")

if __name__ == "__main__":
    main()
