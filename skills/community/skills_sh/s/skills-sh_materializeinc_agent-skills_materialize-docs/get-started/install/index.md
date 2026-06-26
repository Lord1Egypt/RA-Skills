# Install Self-Managed Materialize
Install Self-Managed Materialize.
<p>You can install Self-Managed Materialize on a Kubernetes cluster running
locally or on a cloud provider. Self-Managed Materialize requires:</p>
<ul>
<li>A Kubernetes (v1.31+) cluster.</li>
<li>PostgreSQL as a metadata database.</li>
<li>Blob storage.</li>
<li>A license key.</li>
</ul>
<h2 id="license-key">License key</h2>
<p>Starting in v26.0, Materialize requires a license key.</p>

| License key type | Deployment type | Action |
| --- | --- | --- |
| Community | New deployments | <p>To get a license key:</p> <ul> <li>If you have a Cloud account, visit the <a href="https://console.materialize.com/license/" ><strong>License</strong> page in the Materialize Console</a>.</li> <li>If you do not have a Cloud account, visit <a href="https://materialize.com/self-managed/community-license/" >https://materialize.com/self-managed/community-license/</a>.</li> </ul> |
| Community | Existing deployments | Contact <a href="https://materialize.com/docs/support/" >Materialize support</a>. |
| Enterprise | New deployments | Visit <a href="https://materialize.com/self-managed/enterprise-license/" >https://materialize.com/self-managed/enterprise-license/</a> to purchase an Enterprise license. |
| Enterprise | Existing deployments | Contact <a href="https://materialize.com/docs/support/" >Materialize support</a>. |

<h2 id="installation-guides">Installation guides</h2>
<p>The following installation guides are available to help you get started:</p>

<h3 id="install-using-helm-commands">Install using Helm Commands</h3>
<table>
  <thead>
      <tr>
          <th>Guide</th>
          <th>Description</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-local-kind/" >Install locally on Kind</a></td>
          <td>Uses standard Helm commands to deploy Materialize to a Kind cluster in Docker.</td>
      </tr>
  </tbody>
</table>

<h3 id="install-using-terraform-modules">Install using Terraform Modules</h3>
> **Note:** We recommend pinning your module sources to specific tags to avoid unexpected breaking
> changes in future versions.
> We recommend updating your module source tags when updating Materialize versions,
> taking care to follow any instructions in the release notes.

<table>
  <thead>
      <tr>
          <th>Guide</th>
          <th>Description</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-aws/" >Install on AWS</a></td>
          <td>Uses Terraform module to deploy Materialize to AWS Elastic Kubernetes Service (EKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-azure/" >Install on Azure</a></td>
          <td>Uses Terraform module to deploy Materialize to Azure Kubernetes Service (AKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-gcp/" >Install on GCP</a></td>
          <td>Uses Terraform module to deploy Materialize to Google Kubernetes Engine (GKE).</td>
      </tr>
  </tbody>
</table>

<h3 id="install-using-legacy-terraform-modules">Install using Legacy Terraform Modules</h3>
> **Note:** We recommend pinning your module sources to specific tags to avoid unexpected breaking
> changes in future versions.
> We recommend updating your module source tags when updating Materialize versions,
> taking care to follow any instructions in the release notes.

<table>
  <thead>
      <tr>
          <th>Guide</th>
          <th>Description</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="/self-managed-deployments/installation/legacy/install-on-aws-legacy/" >Install on AWS (Legacy Terraform)</a></td>
          <td>Uses legacy Terraform module to deploy Materialize to AWS Elastic Kubernetes Service (EKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/legacy/install-on-azure-legacy/" >Install on Azure (Legacy Terraform)</a></td>
          <td>Uses legacy Terraform module to deploy Materialize to Azure Kubernetes Service (AKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/legacy/install-on-gcp-legacy/" >Install on GCP (Legacy Terraform)</a></td>
          <td>Uses legacy Terraform module to deploy Materialize to Google Kubernetes Engine (GKE).</td>
      </tr>
  </tbody>
</table>

