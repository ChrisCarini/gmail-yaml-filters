# gmail-yaml-filters

[![Build Status](https://github.com/mesozoic/gmail-yaml-filters/workflows/Tests/badge.svg?branch=master)](https://github.com/mesozoic/gmail-yaml-filters/actions?workflow=Tests)

A quick tool for generating Gmail filters from YAML rules.

Interested in helping? See [CONTRIBUTING.md](CONTRIBUTING.md) for a few guidelines.

## Getting Started

It's strongly recommended to use a tool like [pipx](https://pypa.github.io/pipx/)
to install this package in an isolated environment:

```bash
$ pipx install gmail-yaml-filters
```

## Generating XML

By default, the command line script will generate XML to stdout, which
you can then upload to Gmail yourself:

```bash
$ gmail-yaml-filters my-filters.yaml > my-filters.xml
```

## Synchronization via Gmail API

If you are the trusting type, you can authorize the script to
upload new filters and remove obsolete filters via Gmail's API.
Before using any of these commands, you will need to follow the
steps below to [Create `client_secret.json`](#creating-client_secretsjson).

```bash
# Upload all filters (and create new labels) from the configuration file
$ gmail-yaml-filters --upload my-filters.yaml

# Delete any filters that aren't defined in the configuration file
$ gmail-yaml-filters --prune my-filters.yaml

# Do both of these steps at once.
$ gmail-yaml-filters --sync my-filters.yaml

# See what would happen but don't apply any changes.
$ gmail-yaml-filters --dry-run --sync my-filters.yaml

# Delete all your filters. (Yikes!)
$ gmail-yaml-filters --delete-all
```

If you need to pipe configuration from somewhere else, you can do that
by passing a single dash as the filename.

```sh
# (but why would you need to do this?)
$ cat filters.yaml | gmail-yaml-filters --sync -
```

## Sample Configuration

```yaml
# Simple example
-
  from: googlealerts-noreply@google.com
  label: news
  not_important: true

# Boolean conditions
-
  from:
    any:
      - alice
      - bob
      - carol
  to:
    all: [me, -MyBoss]
  label: conspiracy

# Nested conditions
-
  from: lever.co
  label: hiring
  more:
    -
      has: 'completed feedback'
      archive: true
    -
      has: 'what is your feedback'
      star: true
      important: true

# Foreach loops
-
  for_each:
    - list1
    - list2
    - list3
  rule:
    to: "{item}@mycompany.com"
    label: "{item}"

# Foreach loops with complex structures
-
  for_each:
    - [mailing-list-1a, list1]
    - [mailing-list-1b, list1]
    - [mailing-list-1c, list1]
    - [mailing-list-2a, list2]
    - [mailing-list-2b, list2]
  rule:
    to: "{item[0]}@mycompany.com"
    label: "{item[1]}"
-
  for_each:
    - {list: list1, domain: example.com}
    - {list: list2, domain: whatever.com}
  rule:
    to: "{list}@{domain}"
    label: "{list}"
```

## Configuration

Supported conditions:

* `has` (also `match`)
* `does_not_have` (also `missing`, `no_match`)
* `subject`
* `list`
* `labeled`
* `from`, `to`, `cc`, and `bcc`
* `category`
* `deliveredto`
* `filename`
* `larger`
* `smaller`
* `size`
* `rfc822msgid`
* `is` and `has` work like [Gmail's search operators](https://support.google.com/mail/answer/7190?hl=en), for example:
  * `has: attachment` is translated to `match: "has:attachment"`
  * `is: -snoozed` is translated to `no_match: "is:snoozed"`

Supported actions:

* `archive`
* `forward`
* `important` (also `mark_as_important`)
* `label`, including support for Gmail's [category tabs](https://developers.google.com/gmail/api/guides/labels):
  * `CATEGORY_PERSONAL`
  * `CATEGORY_SOCIAL`
  * `CATEGORY_PROMOTIONS`
  * `CATEGORY_UPDATES`
  * `CATEGORY_FORUMS`
* `not_important` (also `never_mark_as_important`)
* `not_spam`
* `read` (also `mark_as_read`)
* `star`
* `trash` (also `delete`)

Any set of rules with `ignore: true` will be ignored and not written to XML.

## Creating `client_secrets.json`

Follow the steps [found here to create a `client_secret.json`](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred).

We recommend setting the below:

| Option                        | Value                         |
|-------------------------------|-------------------------------|
| Application Type              | `Web application`             |
| Name                          | `mesozoic/gmail-yaml-filters` |
| Authorized JavaScript origins | _Empty_                       |
| Authorized redirect URIs      | `http://localhost:8080/`      |

Once you have clicked the `Create` button, click `Download JSON` on the dialog that appears. 
Save this file as `client_secret.json` to the base directory of this project.

## Similar Projects

* [gmail-britta](https://github.com/antifuchs/gmail-britta) is written in Ruby and lets you express rules with a DSL.
* [gmail-filters](https://github.com/dimagi/gmail-filters) is written in Python and has a web frontend.
* [google-mail-filter](https://hackage.haskell.org/package/google-mail-filters) is written in Haskell and lets you express rules with a DSL.
