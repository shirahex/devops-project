# 🚀 DevOps Final Project — Master DSBD & IA

**Stack**: Flask API · Docker · GitHub Actions · Kubernetes · Terraform · Ansible · Prometheus · Grafana

---

## 📁 Project Structure

```
devops-project/
├── app/                        # Flask REST API + tests
│   ├── app.py
│   ├── test_app.py
│   └── requirements.txt
├── docker/                     # Containerization
│   ├── Dockerfile
│   ├── .dockerignore
│   └── docker-compose.yml
├── k8s/                        # Kubernetes manifests
│   ├── deployment.yaml         # Deployment + Service + ConfigMap
│   ├── hpa.yaml                # HorizontalPodAutoscaler
│   └── ingress.yaml
├── terraform/                  # AWS infrastructure as code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── ansible/                    # Configuration management
│   ├── inventory.ini
│   ├── 01-common.yml           # Docker + K8s install (all nodes)
│   ├── 02-master.yml           # kubeadm init + Flannel CNI
│   ├── 03-workers.yml          # Join worker nodes
│   └── 04-deploy-app.yml       # Deploy app to cluster
├── monitoring/
│   └── monitoring-stack.yml    # Prometheus + Grafana
└── .github/workflows/
    └── ci-cd.yml               # Full CI/CD pipeline
```

---

## ⚡ Quick Start

### 1. Prerequisites (local machine)
```bash
# Install tools
brew install terraform ansible awscli   # macOS
# OR
sudo apt install terraform ansible awscli  # Ubuntu

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret, Region (us-east-1), output (json)

# Generate SSH key (if not already)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

### 2. Provision AWS with Terraform
```bash
cd terraform/

# Initialize Terraform
terraform init

# Preview what will be created
terraform plan

# Create 2 EC2 instances (master + worker)
terraform apply

# Note the outputs:
# master_public_ip = "x.x.x.x"
# worker_public_ip = "x.x.x.x"
```

### 3. Update Ansible Inventory
Edit `ansible/inventory.ini` and replace:
- `MASTER_PUBLIC_IP` → value from terraform output
- `WORKER_PUBLIC_IP` → value from terraform output

```bash
# Test connectivity
ansible -i ansible/inventory.ini k8s_cluster -m ping
```

### 4. Configure Kubernetes with Ansible
```bash
cd ansible/

# Step 1: Install Docker + K8s on all nodes
ansible-playbook -i inventory.ini 01-common.yml

# Step 2: Init master node
ansible-playbook -i inventory.ini 02-master.yml

# Step 3: Join worker node
ansible-playbook -i inventory.ini 03-workers.yml
```

### 5. Set Up GitHub Actions Secrets

In your GitHub repo → Settings → Secrets → Actions, add:

| Secret | Value |
|--------|-------|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token |
| `KUBECONFIG` | Base64 of `~/.kube/config` from master |

```bash
# Get KUBECONFIG secret value:
ssh ubuntu@MASTER_IP "cat ~/.kube/config" | base64
```

### 6. Update K8s manifests

In `k8s/deployment.yaml`, replace:
```
image: YOUR_DOCKERHUB_USERNAME/devops-api:latest
```
with your actual DockerHub username.

### 7. Initial Manual Deploy (first time)
```bash
ansible-playbook -i ansible/inventory.ini ansible/04-deploy-app.yml \
  -e "docker_image=YOUR_DOCKERHUB_USERNAME/devops-api:latest"
```

---

## 🔄 CI/CD Demo Flow (for presentation)

The pipeline triggers automatically on every push to `main`:

```
git push → GitHub Actions triggers →
  1. Tests run (pytest)
  2. Docker image built & pushed to DockerHub
  3. kubectl rollout to Kubernetes
  4. Zero-downtime rolling update
```

**Live demo command:**
```bash
# Make a visible change in app.py, then:
git add .
git commit -m "feat: update API message for demo"
git push origin main
# Watch GitHub Actions tab → then verify on cluster
kubectl get pods -n devops-app -w
```

---

## 📊 Monitoring (Optional)

```bash
# Deploy Prometheus + Grafana
kubectl apply -f monitoring/monitoring-stack.yml

# Get Grafana NodePort
kubectl get svc grafana-service -n monitoring

# Access: http://MASTER_IP:NODEPORT
# Login: admin / admin123
```

---

## 🧹 Clean Up (important — avoid AWS charges!)

```bash
cd terraform/
terraform destroy
```

---

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info + version |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/:id` | Update a task |
| DELETE | `/tasks/:id` | Delete a task |

**Test locally:**
```bash
docker-compose -f docker/docker-compose.yml up
curl http://localhost:5000/health
curl http://localhost:5000/tasks
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New DevOps task"}'
```
