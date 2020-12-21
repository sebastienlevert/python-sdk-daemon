# A simple Python daemon console application calling Microsoft Graph with its own identity (client secret variation)

## About this sample

### Overview

This sample application shows how to use the [Microsoft identity platform endpoint](http://aka.ms/aadv2) to access the data of Microsoft business customers in a long-running, non-interactive process.  It uses the [OAuth 2 client credentials grant](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow) to acquire an access token, which can be used to call the [Microsoft Graph](https://graph.microsoft.io) and access organizational data

The app is Python Console application. It gets the list of users in an Azure AD tenant by using `Microsoft Graph Python Client Library` to acquire a token.

## Scenario

The console application:

- gets a token from microsoft identity platform in its own name (without a user)
- calls the Microsoft Graph /users endpoint to get the list of user, which it then displays (as Json blob)
- and then calls the Microsoft Graph /users/{user-id}/sendMail endpoint to send an email on behalf of the first user found from that user

For more information on the concepts used in this sample, be sure to read the [Daemon app scenario](https://docs.microsoft.com/azure/active-directory/develop/scenario-daemon-overview) and, if you're insterested in protocol details, the [Microsoft identity platform endpoint client credentials protocol documentation](https://azure.microsoft.com/documentation/articles/active-directory-v2-protocols-oauth-client-creds).

> ### Daemon applications can use two forms of secrets to authenticate themselves with Azure AD:
>
> - **application secrets** (this Readme.md).
> - **certificates**, in the [../2-Call-MsGraph-WithCertificate](../2-Call-MsGraph-WithCertificate) folder

## How to run this sample

To run this sample, you'll need:

> - [Python 2.7+](https://www.python.org/downloads/release/python-2713/) or [Python 3+](https://www.python.org/downloads/release/python-364/)
> - An Azure Active Directory (Azure AD) tenant. For more information on how to get an Azure AD tenant, see [how to get an Azure AD tenant.](https://docs.microsoft.com/azure/active-directory/develop/quickstart-create-new-tenant)

### Step 1:  Clone or download this repository

From your shell or command line:

```Shell
git clone https://github.com/sebastienlevert/python-sdk-core-daemon.git
```

Go to the `"1-Call-MsGraph-WithSecret"` folder

```Shell
cd "01-Call-MsGraph-WithSecret"
```

or download and exact the repository .zip file.

> Given that the name of the sample is pretty long, you might want to clone it in a folder close to the root of your hard drive, to avoid file size limitations on Windows.

### Step 2:  Register the sample with your Azure Active Directory tenant

There is one project in this sample. To register it, you can:

- either follow the steps [Step 2: Register the sample with your Azure Active Directory tenant](#step-2-register-the-sample-with-your-azure-active-directory-tenant) and [Step 3:  Configure the sample to use your Azure AD tenant](#choose-the-azure-ad-tenant-where-you-want-to-create-your-applications)
- or use PowerShell scripts that:
  - **automatically** creates the Azure AD applications and related objects (passwords, permissions, dependencies) for you
  - modify the Visual Studio projects' configuration files.

If you want to use this automation:

1. Run the sample

   You'll need to install the dependencies using pip as follows:
  
   ```Shell
    pip install -r requirements.txt
    ```

    Run `confidential_client_secret_sample.py` with the parameters for the app:

   ```Shell
   python confidential_client_secret_sample.py parameters.json
   ```

If ou don't want to use this automation, follow the steps below

#### Choose the Azure AD tenant where you want to create your applications

As a first step you'll need to:

1. Sign in to the [Azure portal](https://portal.azure.com) using either a work or school account or a personal Microsoft account.
1. If your account is present in more than one Azure AD tenant, select `Directory + Subscription` at the top right corner in the menu on top of the page, and switch your portal session to the desired Azure AD tenant.
1. In the left-hand navigation pane, select the **Azure Active Directory** service, and then select **App registrations**.

#### Register the client app (daemon-console)

1. Navigate to the Microsoft identity platform for developers [App registrations](https://go.microsoft.com/fwlink/?linkid=2083908) page.
1. Select **New registration**.
   - In the **Name** section, enter a meaningful application name that will be displayed to users of the app, for example `python-sdk-daemon`.
   - In the **Supported account types** section, select **Accounts in this organizational directory only ({tenant name})**.
   - Select **Register** to create the application.
1. On the app **Overview** page, find the **Application (client) ID** value and record it for later. You'll need it to configure the Visual Studio configuration file for this project.
1. From the **Certificates & secrets** page, in the **Client secrets** section, choose **New client secret**:

   - Type a key description (of instance `app secret`),
   - Select a key duration of either **In 1 year**, **In 2 years**, or **Never Expires**.
   - When you press the **Add** button, the key value will be displayed, copy, and save the value in a safe location.
   - You'll need this key later to configure the project in Visual Studio. This key value will not be displayed again, nor retrievable by any other means,
     so record it as soon as it is visible from the Azure portal.
1. In the list of pages for the app, select **API permissions**
   - Click the **Add a permission** button and then,
   - Ensure that the **Microsoft APIs** tab is selected
   - In the *Commonly used Microsoft APIs* section, click on **Microsoft Graph**
   - In the **Application permissions** section, ensure that the right permissions are checked: **User.Read.All**, **Mail.Send**
   - Select the **Add permissions** button

1. At this stage permissions are assigned correctly but the client app does not allow interaction.
   Therefore no consent can be presented via a UI and accepted to use the service app.
   Click the **Grant/revoke admin consent for {tenant}** button, and then select **Yes** when you are asked if you want to grant consent for the
   requested permissions for all account in the tenant.
   You need to be an Azure AD tenant admin to do this.

### Step 3:  Configure the sample to use your Azure AD tenant

In the steps below, "ClientID" is the same as "Application ID" or "AppId".

Open the parameters.json file

#### Configure the client project

1. Open the `parameters.json` file
1. Find the string key `%YOUR_TENANT_ID%` and replace the existing value with the directlry (tenant) ID of the `python-sdk-daemon` application copied from the Azure portal. (Example : b61f9af1-d6cf-4cc0-a6f6-befb38bc00ae)
1. Find the string key `%YOUR_CLIENT_ID%` and replace the existing value with the application ID (clientId) of the `python-sdk-daemon` application copied from the Azure portal. (Example : faddf6f2-ec3f-4923-9bb1-bdf7c2656b78)
1. Find the string key `%YOUR_CLIENT_SECRET%` and replace the existing value with the key you saved during the creation of the `python-sdk-daemon` app, in the Azure portal. (Example : 23y3ky5qX6E.5e_3T7sJLs.41oCBf-m2LK)
1. Find the string key `%YOUR_SAMPLE_USER%` and replace the existing value with the user you want to print on the screen and use to send emails. (Example : admin@contoso.onmicrosoft.com)

### Step 4: Run the sample

You'll need to install the dependencies using pip as follows:
  
```Shell
pip install -r requirements.txt
```

Start the application, it will display some Json string containing the users in the tenant.

```Shell
python confidential_client_secret_sample.py parameters.json
```