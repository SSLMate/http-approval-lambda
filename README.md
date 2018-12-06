# SSLMate HTTP Approval for Application Load Balancers

This serverless application enables you to configure your Application
Load Balancer to automatically approve SSLMate certificates for
domains that are pointed at your load balancer.  This lets you
automatically issue and renew certificates for these domains without any
user interaction.  [Learn more about SSLMate's HTTP approval](https://sslmate.com/help/approval/http).


## Setup instructions

1. Deploy the application:

	1. Visit <https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:485511610825:applications~sslmate-http-approval> and click **Deploy**.

	2. Select the AWS region in which your ALB is located.

	3. Under "Application Settings", enter the URL of your SSLMate HTTP
	Approval Proxy.  You can find this URL on your [SSLMate account's API
	credentials page](https://sslmate.com/account/api_credentials).  The URL
	looks like `https://3.http-approval.sslmate.com`.

	4. Click **Deploy**.

2. Create a Target Group for the application:

	1. Open the Target Groups page under your EC2 Dashboard and click **Create target group**.

	2. Enter the target group name `sslmate-http-approval`.
	
	3. Select the **Lambda function** target type.
	
	4. Select the newly-created Lambda function (the name looks like `aws-serverless-repository-sslm-sslmatehttpapproval-1VY7IG21WDOEM`).
	
	5. Select the `$LATEST` version.

	6. Click **Create**.

3. Create forwarding rules for `/.well-known/acme-challenge/` and `/.well-known/pki-validation/`:

	1. Open the Load Balancers page under your EC2 Dashboard, select your ALB, click the Listeners tab,
	and then click `View/edit rules` under the port 80 listener.

	2. Add the following two rules:

		* If Path is ` /.well-known/acme-challenge/*`, then Forward to `sslmate-http-approval`.
		* If Path is ` /.well-known/pki-validation/*`, then Forward to `sslmate-http-approval`.

	3. Click **Save**.

4. Test that your integration is correctly configured using the [HTTP approval test tool](https://sslmate.com/account/http_approval).
