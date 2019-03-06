const { join } = require('path')
const QuickgRPC = require('quick-grpc')

async function go () {
  const { oakLights } = await new QuickgRPC({
    host: 'localhost:9100',
    basePath: join(__dirname, '..')
  })
  let lights = await oakLights()
  lights.info(undefined, function (err, data) {
    if (err) throw err
    console.log('Oak Lights Info:', JSON.stringify(data, null, 2))
    if (!data.controllers.length) {
      console.log('No light controllers found')
    } else {
      const lightControllerId = data.controllers[0].controllerId
      let req = {
        controllerId: lightControllerId,
        hex: '#AA0000',
        duration: 1000
      }
      console.log('ChangeColor Request:', req)
      lights.ChangeColor(req, function (err, data) {
        if (err) throw err
        setTimeout(() => {
          let req = {
            controllerId: lightControllerId,
            hex: '#00AA00',
            duration: 1000
          }
          console.log('ChangeColor Request:', req)
          lights.ChangeColor(req, function (err, data) {
            if (err) throw err
          })
        }, 2000)
      })
    }
  })
}

go()
