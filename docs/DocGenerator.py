opsConfigFieldsDocMap = [
{
    "key"   : "PlaMode",
    "scope" : ["pla","plafull","dd","tr","trfull","raj"],
    "doc"   : F("""\
                Description
                    Player software supports multiple modes of operation.
                    This field configures the software to a specific operational mode.

                Supported values
                * pl
                * dd
                * tr

                This is a mandatory field.
                Example
                    PlaMode = dd""")
},
{
    "key"   : "EnableOpsConfig",
    "scope" : ["player","playerfull","doordarshan","transcoder","transcoderfull"],
    "doc"   : F("""\
                Description
                    The enables or disables usage of CMS
                    software for generation Cloudport Player configurations.

                Supported values
                * true
                * false

                This is a mandatory field.
                When in doubt, configure to true.

                Example
                    EnableOpsConfig = true""")
},
{
    "key"   : "EnableOpsConfig",
    "scope" : ["pla","plafull","dd","tr","trfull"],
    "doc"   : F("""\
                Description
                    The configuration enables or disables usage of CMS
                    software for generation Cloudport Player configurations.

                Supported values
                * true
                * false

                This is a mandatory field.
                When in doubt, configure to true.

                Example
                    EnableOpsConfig = true""")
}
]