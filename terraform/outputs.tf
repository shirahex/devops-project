output "master_public_ip" {
  description = "Public IP of the Kubernetes master node"
  value       = aws_instance.master.public_ip
}

output "worker_public_ip" {
  description = "Public IP of the Kubernetes worker node"
  value       = aws_instance.worker.public_ip
}

output "master_private_ip" {
  description = "Private IP of the master (used for kubeadm join)"
  value       = aws_instance.master.private_ip
}

output "ssh_master" {
  description = "SSH command for master node"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_instance.master.public_ip}"
}

output "ssh_worker" {
  description = "SSH command for worker node"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_instance.worker.public_ip}"
}
